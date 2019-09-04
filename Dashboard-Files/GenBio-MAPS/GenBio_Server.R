DownloadClassData <- function(input, output, session, data) {
  
  data.class <- reactive({
    data.class <- subset(data, Class_ID == input$classID)
    return(data.class)
  })
  
  output$downloadData <- downloadHandler(
    filename = function (){
      paste("EcoEvo-MAPS_", input$classID, ".csv", sep = "")
    },
    content = function(file) {
      write.csv(data.class() %>%
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
      Scores.cols <- c('SC_T_Ecology', 'SC_T_Evolution', 'SC_Total_Score')
      Labels <- c('Ecology', 'Evolution', 'Total Score')
    } else if(input$scale == 'Vision and Change') {
      Scores.cols <- c('SC_VC_Evolution', 'SC_VC_Information_Flow', 'SC_VC_Structure_Function',
                      'SC_VC_Transformations_of_Energy_and_Matter', 'SC_VC_Systems')
      Labels <- c('Evolution', 'Information Flow', 'Structure/Function',
                  'Transformations of\nEnergy and Matter', 'Systems')
    } else if(input$scale == 'Ecology and Evolution Core Concepts') {
      Scores.cols <- c('SC_EE_Heritable_Variation', 'SC_EE_Modes_of_Change',
                      'SC_EE_Phylogeny_and_Evolutionary_History', 'SC_EE_Biological_Diversity',
                      'SC_EE_Populations', 'SC_EE_Energy_and_Matter',
                      'SC_EE_Interactions_with_Ecosystems', 'SC_EE_Human_Impact')
      Labels <- c('Heritable\nVariation', 'Modes of\nChange', 'Phylogeny and\nEvolutionary History', 
                  'Biological\nDiversity', 'Populations', 'Energy\nand Matter', 
                  'Interactions\nwith Ecosystems', 'Human\nImpact')
    } else {
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
    if(!is.null(Class.var)) {
      Scores.cols <- c(Scores.cols, Class.var)
      data.scale <- data.temp[, Scores.cols] %>%
        group_by_(Class.var) %>%
        melt(.)
      p <- ggplot(data.scale, aes_string(x = 'variable', y = 'value', color = Class.var))
    } else {
      Demographic <- reactive({
        Demographic <- Demographitize(input$demographic)
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

ResponsesPlot <- function(input, output, session, data, Demo = NULL, Class.var = NULL){
  if(!is.null(Demo)){
    Demographic <- reactive({
      Demographic <- Demographitize(Demo())
    })
    Responses.df <- reactive({
      if(Demographic() == 'None'){
        Responses.df <- data() %>%
          select(c(grep(paste('^(', input$question, '_[0-9]*S$)', sep = ''), names(.)))) %>% 
          replace(is.na(.), 0) %>%
          summarize_all(funs(mean)) %>%
          melt(.)
      } else {
        data.temp <- data.frame(data())
        Responses.df <- data.temp[data.temp[, Demographic()] != '',] %>%
          select(c(grep(paste('^(', input$question, '_[0-9]*S$)', sep = ''), names(.))), 
                 Demographic()) %>% 
          replace(is.na(.), 0) %>%
          group_by_(Demographic()) %>%
          summarize_all(funs(mean)) %>%
          melt(.)
        Responses.df <- Responses.df[!is.na(Responses.df[, Demographic()]),]
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
        select(c(grep(paste('^(', input$question, '_[0-9]*S$)', sep = ''), names(.))), 
               Class.var) %>% 
        replace(is.na(.), 0) %>%
        group_by_(Class.var) %>%
        summarize_all(funs(mean)) %>%
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


Demographitize <- function(demo){
  Demo <- case_when(demo == 'Gender' ~ 'Gender',
                    demo == 'Major' ~ 'Major',
                    demo == 'URM Status' ~ 'URM_Status',
                    demo == 'Class Standing' ~ 'Class_Standing',
                    demo == 'First Generation Status' ~ 'First_Gen_Status',
                    TRUE ~ 'None')
  return(Demo)
}