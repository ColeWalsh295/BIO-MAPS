DownloadClassData <- function(input, output, session, data) {
  
  data.class <- reactive({
    data.class <- subset(data, Course == input$classID)
    return(data.class)
  })
  
  observeEvent(input$classID, {
    toggleState("downloadData", condition = !data.class()[1, 'Data_Available'])
    # if(!data.class()[1, 'Data_Available']){
    #   shinyalert("Oops!", "There are too few students the dataset.", type = "error")
    # } else {
    #   DisableRadio(data.class)
    # }
  })
  
  data.out <- reactive({
    data.out <- data.class() %>%
      mutate(Class = ifelse(Class_Avail_Down, Class, NA_character_),
             Trans = ifelse(Trans_Avail_Down, Trans, NA_character_),
             Maj = ifelse(Maj_Avail_Down, Maj, NA_character_),
             Gen = ifelse(Gen_Avail_Down, Gen, NA_character_),
             Eng = ifelse(Eng_Avail_Down, Eng, NA_character_),
             Educ = ifelse(Educ_Avail_Down, Educ, NA_character_),
             Ethn = ifelse(Ethn_Avail_Down, Ethn, NA_character_))
    return(data.out)
  })
  
  output$downloadData <- downloadHandler(
    filename = function (){
      paste("GenBio-MAPS_", input$classID, ".csv", sep = "")
    },
    content = function(file) {
      write.csv(data.out() %>%
                  select(-c('N.Students')), file, row.names = FALSE)
    }
  )
  return(data.class)
}

ClassStatistics <- function(input, output, session, data, Overall = FALSE){
  output$infoNStudents <- renderInfoBox({
    if(!Overall){
      infoBox(HTML("Number of<br>Students"),
              data()$N.Students[1],
              icon = icon("list"), color = "blue", width = 12)
    } else {
      infoBox(HTML("Number of<br>Students"),
              sum(data()[!duplicated(data()$Class_ID), 'N.Students']),
              icon = icon("list"), color = "blue", width = 12)
    }
  })
  
  output$infoScore = renderInfoBox({
    infoBox(HTML("Average<br>Score"),
            paste(data() %>%
                    summarize(Avg = round(mean(SC_Total_Score), 3) * 100) %>%
                    pull(), '%'),
            icon = icon("list"), color = "orange")
  })
}

ScalePlot <- function(input, output, session, data, Class.var = NULL){
  output$plotScale = renderPlot({
    data.temp <- data.frame(data())
    if(input$scale == 'Overall Scores') {
      Scores.cols <- c('SC_T_Cellular_and_Molecular', 'SC_T_Physiology', 
                       'SC_T_Ecology_and_Evolution', 'SC_Total_Score')
      Labels <- c('Cellular and Molecular', 'Physiology', 'Ecology and Evolution', 'Total Score')
    } else {
      Scores.cols <- c('SC_VC_Evolution', 'SC_VC_Information_Flow', 'SC_VC_Structure_Function',
                      'SC_VC_Transformations_of_Energy_and_Matter', 'SC_VC_Systems')
      Labels <- c('Evolution', 'Information Flow', 'Structure/Function',
                  'Transformations of\nEnergy and Matter', 'Systems')
    }
    
    if(!is.null(Class.var)) {
      Scores.cols <- c(Scores.cols, Class.var)
      data.scale <- data.temp[, Scores.cols] %>%
        group_by_(Class.var) %>%
        melt(.)
      p <- ggplot(data.scale, aes_string(x = 'variable', y = 'value', color = Class.var))
    } else {
      Demographic <- reactive({
        Demographic <- input$demographic
      })
      if(Demographic() == 'None'){
        data.scale <- data.temp[, Scores.cols] %>%
          melt(.)
        p <- ggplot(data.scale, aes(x = variable, y = value))
      } else {
        Scores.cols <- c(Scores.cols, Demographic())
        data.scale <- data.temp[data.temp[, Demographic()] != '', Scores.cols] %>%
          group_by_(Demographic()) %>%
          melt(.)
        p <- ggplot(data.scale, aes_string(x = 'variable', y = 'value', color = Demographic())) +
          labs(color = input$demographic)
      }
    }
    p <- p + geom_boxplot(lwd = 1) +
      labs(x = input$scale, y = 'Score', title = "Your students' performance") +
      scale_x_discrete(labels = Labels) +
      scale_color_manual(values = c("#0072b2", "#d55e00", "#009e73", "#cc79a7")) +
      shiny_theme
    if(length(Labels) > 8){
      p <- p + coord_flip()
    }
    return(p)
  })
  if(is.null(Class.var)){
    return(reactive(input$demographic))
  }
}

ResponsesPlot <- function(input, output, session, data, Demographic = NULL, Class.var = NULL){
  if(!is.null(Demographic)){
    Responses.df <- reactive({
      if(Demographic() == 'None'){
        Responses.df <- data() %>%
          select(c(grep(paste('^(BM-', input$question, '_[0-9]*S$)', sep = ''), names(.)))) %>%
          summarize_all(funs(mean), na.rm = TRUE) %>%
          melt(.)
      } else {
        Responses.df <- data() %>%
          select(c(grep(paste('^(BM-', input$question, '_[0-9]*S$)', sep = ''), names(.))), Demographic()) %>%
          group_by_(Demographic()) %>%
          summarize_all(funs(mean), na.rm = TRUE) %>%
          melt(.)
        Responses.df <- Responses.df[Responses.df[, Demographic()] != '',]
      }
      return(Responses.df)
    })
    output$plotResponses = renderPlot({
      if(Demographic() != 'None'){
        p <- ggplot(Responses.df(), aes_string(x = 'variable', y = 'value', fill = Demographic()))
      } else {
        p <- ggplot(Responses.df(), aes(x = variable, y = value))
      }
      p <- p + geom_bar(stat = 'identity', position = 'dodge') +
        coord_flip() +
        labs(x = 'Statement', y = 'Fraction of Correct Selections', 
             title = "Your students' selections") +
        scale_fill_manual(values = c("#0072b2", "#d55e00", "#009e73", "#cc79a7")) +
        shiny_theme

      return(p)
    })
  } else {
    Responses.df <- reactive({
      Responses.df <- data() %>%
        select(c(grep(paste('^(BM-', input$question, '_[0-9]*S$)', sep = ''), names(.))), 
               Class.var) %>%
        group_by_(Class.var) %>%
        summarize_all(funs(mean), na.rm = TRUE) %>%
        melt(.)
      return(Responses.df)
    })
    output$plotResponses = renderPlot({
      p <- ggplot(Responses.df(), aes_string(x = 'variable', y = 'value', fill = Class.var)) +
        geom_bar(stat = 'identity', position = 'dodge') +
        coord_flip() +
        labs(x = 'Statement', y = 'Fraction of Correct Selections', 
             title = "Your students' selections") +
        scale_fill_manual(values = c("#0072b2", "#d55e00", "#009e73", "#cc79a7")) +
        shiny_theme
      return(p)
    })
  }
}

DisableRadio <- function(df){
  for(Option in c('Gen', 'Ethn', 'Educ', 'Class', 'Maj', 'Trans', 'Eng')){
    if(!isTRUE(df()[1, paste(Option, '_Avail_Radio', sep = '')])){
      shinyjs::runjs(paste("$('[type = radio][value = ", Option, "]').parent().parent().css('opacity', 0.4)", sep = ''))
      shinyjs::runjs(paste("$('[type = radio][value = ", Option, "]').prop('disabled', true)", sep = ''))
    } else {
      shinyjs::runjs(paste("$('[type = radio][value = ", Option, "]').parent().parent().css('opacity', 1)", sep = ''))
      shinyjs::runjs(paste("$('[type = radio][value = ", Option, "]').prop('disabled', false)", sep = ''))
      }
  }
  return(0)  
}