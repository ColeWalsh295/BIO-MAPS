DownloadClassData <- function(input, output, session, data, header, cols, ass) {
  
  observe({
    if(ass() == 'GenBio-MAPS'){
      updateTextInput(session, 'classID', value = 'R_0vU5WDrHWLjYc37')
    } else {
      updateTextInput(session, 'classID', value = 'R_6WkTbfUv4dUhh5f')
    }
  })
  
  data.class <- eventReactive(input$classID, {
    data.class <- subset(data(), Class_ID == input$classID)
    return(data.class)
  })
  
  observeEvent(input$classID, ({
    if(!data.class()[1, 'Data_Available']){
      shinyalert("Oops!", "There are too few students the dataset.", type = "error")
      disable('downloadData')
    } else {
      enable('downloadData')
      DisableRadio(data.class)
    }
  }))
  
  data.out <- reactive({
    data.out <- data.class() %>%
      mutate(Class = ifelse(Class_Avail_Down, Class, NA_character_),
             Trans = ifelse(Trans_Avail_Down, Trans, NA_character_),
             Maj = ifelse(Maj_Avail_Down, Maj, NA_character_),
             Gen = ifelse(Gen_Avail_Down, Gen, NA_character_),
             Eng = ifelse(Eng_Avail_Down, Eng, NA_character_),
             Educ = ifelse(Educ_Avail_Down, Educ, NA_character_),
             Ethn = ifelse(Ethn_Avail_Down, Ethn, NA_character_))
    data.out <- rbind(header()[, cols(), with = FALSE], data.out[, cols()])
    data.out[is.na(data.out)] <- ''
    return(data.out)
  })
  
  output$downloadData <- downloadHandler(
    filename = function (){
      paste(ass(), '_', input$classID, ".csv", sep = "")
    },
    content = function(file) {
      write.csv(data.out(), file, row.names = FALSE)
    }
  )
  
  df.return <- reactive({
    if(as.logical(data.class()[1, 'Data_Available'])){
      df.return <- data.class()
    } else {
      df.return <- data.class()[0, ]
      df.return[1, ] <- NA
    }
    return(df.return)
  })
  return(df.return)
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

ScalePlot <- function(input, output, session, data, ass, Class.var = NULL, compare = FALSE){
  observe({
    if(ass() == 'GenBio-MAPS'){
      scales <- list('Overall Scores', 'Vision and Change')
    } else if(ass() == 'EcoEvo-MAPS') {
      scales <- list('Overall Scores', 'Vision and Change', 'Ecology and Evolution Core Concepts', 
                     '4DEE Framework')
    }
    updateSelectInput(session, "scale", label = "Scale:", choices = scales)
  })
  
  data.out <- reactive({
    if(compare){
      if(input$match){
        Class1 <- subset(data(), Class_ID == levels(factor(data()$Class_ID))[1])
        Class2 <- subset(data(), Class_ID == levels(factor(data()$Class_ID))[2])
        matched.ID <- intersect(Class1$ID, Class2$ID)
        matched.FullName <- intersect(Class1$FullName, Class2$FullName)
        matched.BackName <- intersect(Class1$FullName, Class2$BackName)
        #data.out <- subset(data(), Class_ID %in% Class1$Class_ID)
        data.out <- subset(data(), ID %in% matched.ID)# | FullName %in% matched.FullName | 
         #                    FullName %in% matched.BackName)
      } else {
        data.out <- data()
      }
    } else {
      data.out <- data()
    }
    return(data.out)
  })
  
  output$plotScale = renderPlot({
    data.temp <- data.frame(data.out())
    if((ass() == 'GenBio-MAPS') & (input$scale != 'Vision and Change')) {
      if(input$scale == 'Overall Scores') {
        Scores.cols <- c('SC_T_Cellular_and_Molecular', 'SC_T_Physiology', 
                       'SC_T_Ecology_and_Evolution', 'SC_Total_Score')
        Labels <- c('Cellular and Molecular', 'Physiology', 'Ecology and Evolution', 'Total Score')
      }
    } else if((ass() == 'EcoEvo-MAPS') & (input$scale != 'Vision and Change')) {
      if(input$scale == 'Overall Scores') {
        Scores.cols <- c('SC_T_Ecology', 'SC_T_Evolution', 'SC_Total_Score')
        Labels <- c('Ecology', 'Evolution', 'Total Score')
      } else if(input$scale == 'Ecology and Evolution Core Concepts') {
        Scores.cols <- c('SC_EE_Heritable_Variation', 'SC_EE_Modes_of_Change',
                         'SC_EE_Phylogeny_and_Evolutionary_History', 'SC_EE_Biological_Diversity',
                         'SC_EE_Populations', 'SC_EE_Energy_and_Matter',
                         'SC_EE_Interactions_with_Ecosystems', 'SC_EE_Human_Impact')
        Labels <- c('Heritable\nVariation', 'Modes of\nChange', 'Phylogeny and\nEvolutionary History', 
                    'Biological\nDiversity', 'Populations', 'Energy\nand Matter', 
                    'Interactions\nwith Ecosystems', 'Human\nImpact')
      } else if(input$scale == '4DEE Framework') {
        Scores.cols <- c('SC_FDEE_Populations', 'SC_FDEE_Communities', 'SC_FDEE_Ecosystems',
                         'SC_FDEE_Biomes', 'SC_FDEE_Biosphere', 'SC_FDEE_Quantitative_Reasoning',
                         'SC_FDEE_Designing_and_Critiquing', 'SC_FDEE_Human_Change',
                         'SC_FDEE_Human_Shape', 'SC_FDEE_Matter_and_Energy', 'SC_FDEE_Systems',
                         'SC_FDEE_Space_and_Time')
        Labels <- c('Populations', 'Communities', 'Ecosystems', 'Biomes', 'Biosphere', 
                    'Quantitative reasoning\nand computational thinking', 
                    'Designing and\ncritiquing investigations', 
                    'Human accelerated\nenvironmental change',
                    'Humans shape resources\n/ecosystems/environment', 
                    'Transformations of\nenergy and matter', 'Systems', 'Space\nand Time')
      }
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

ResponsesPlot <- function(input, output, session, data, ass, Demographic = NULL, Class.var = NULL){
  observe({
    if(ass() == 'GenBio-MAPS'){
      questions <- list('01', '02', '03', '04', '07', '08', '12', '13', '14', '15', '16', '18',
                        '19', '20', '21', '22', '23', '24', '27', '28', '30', '31', '32', '33',
                        '35', '36', '37', '38', '40', '43', '44', '45', '49', '50', '54', '55',
                        '59', '60', '61')
    } else if(ass() == 'EcoEvo-MAPS') {
      questions <- list('Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9')
    }
    updateSelectInput(session, "question", label = "Question:", choices = questions)
  })
  
  if(!is.null(Demographic)){
    Responses.df <- reactive({
      if(Demographic() == 'None'){
        Responses.df <- data() %>%
          select(c(grep(paste('^[^T]*', input$question, '_[0-9]*$', sep = ''), names(.)))) %>%
          summarize_all(funs(mean), na.rm = TRUE) %>%
          melt(.)
      } else {
        Responses.df <- data() %>%
          select(c(grep(paste('^[^T]*', input$question, '_[0-9]*$', sep = ''), names(.))), Demographic()) %>%
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
             title = "Your students' performance by statement") +
        scale_fill_manual(values = c("#0072b2", "#d55e00", "#009e73", "#cc79a7")) +
        shiny_theme

      return(p)
    })
  } else {
    Responses.df <- reactive({
      Responses.df <- data() %>%
        select(c(grep(paste('^[^T]*', input$question, '_[0-9]*$', sep = ''), names(.))), 
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
             title = "Your students' performance by statement") +
        scale_fill_manual(values = c("#0072b2", "#d55e00", "#009e73", "#cc79a7")) +
        shiny_theme
      return(p)
    })
  }
}

DisableRadio <- function(df){
  dataFrame <- reactive({
    dataFrame <- data.frame(df())
    return(dataFrame)
  })
  for(Option in c('Gen', 'Ethn', 'Educ', 'Class', 'Maj', 'Trans', 'Eng')){
    if(!dataFrame()[1, paste(Option, '_Avail_Radio', sep = '')]){
      shinyjs::runjs(paste("$('[type = radio][value = ", Option, "]').parent().parent().css('opacity', 0.4)", sep = ''))
      shinyjs::runjs(paste("$('[type = radio][value = ", Option, "]').prop('disabled', true)", sep = ''))
    } else {
      shinyjs::runjs(paste("$('[type = radio][value = ", Option, "]').parent().parent().css('opacity', 1)", sep = ''))
      shinyjs::runjs(paste("$('[type = radio][value = ", Option, "]').prop('disabled', false)", sep = ''))
      }
  }
  return(0)  
}