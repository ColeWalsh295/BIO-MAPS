DownloadClassData <- function(input, output, session, data, header, cols, ass) {
  
  observe({
    if(ass() == 'GenBio-MAPS'){
      updateTextInput(session, 'classID', value = 'R_0vU5WDrHWLjYc37')
    } else if(ass() == 'EcoEvo-MAPS'){
      updateTextInput(session, 'classID', value = 'R_6WkTbfUv4dUhh5f')
    } else if(ass() == 'Phys-MAPS'){
      updateTextInput(session, 'classID', value = 'R_1pLjdulMOPNo3Ka')
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
      mutate(ClassStanding = ifelse(ClassStanding_Avail_Down, ClassStanding, NA_character_),
             TransferStatus = ifelse(TransferStatus_Avail_Down, TransferStatus, NA_character_),
             Major = ifelse(Major_Avail_Down, Major, NA_character_),
             SexGender = ifelse(SexGender_Avail_Down, SexGender, NA_character_),
             ELL = ifelse(ELL_Avail_Down, ELL, NA_character_),
             ParentEducation = ifelse(ParentEducation_Avail_Down, ParentEducation, NA_character_),
             URMStatus = ifelse(URMStatus_Avail_Down, URMStatus, NA_character_))
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
  data.out <- reactive({
    if(Overall) {
      if(input$class.level != 'All'){
        data.out <- subset(data(), Class_Level == input$class.level)
      } else{
        data.out <- data()
      }
    } else {
      data.out <- data()
    }
    return(data.out)
  })

  
  output$infoNStudents <- renderInfoBox({
    if(!Overall){
      infoBox(HTML("Number of<br>Students"),
              data.out()$N.Students[1],
              icon = icon("list"), color = "blue", width = 12)
    } else {
      infoBox(HTML("Number of<br>Students"),
              sum(data.out()[!duplicated(data.out()$Class_ID), 'N.Students']),
              icon = icon("list"), color = "blue", width = 12)
    }
  })
  
  output$infoScore = renderInfoBox({
    infoBox(HTML("Average<br>Score"),
            paste(data.out() %>%
                    summarize(Avg = round(mean(SC_Total_Score), 3) * 100) %>%
                    pull(), '%'),
            icon = icon("list"), color = "orange")
  })
  
  if(Overall){
    return(data.out)
  }
}

ScalePlot <- function(input, output, session, data, ass, class.var = NULL, compare.tab = FALSE){
  observe({
    if((ass() == 'GenBio-MAPS') | (ass() == 'Phys-MAPS')){
      scales <- list('Overall Scores', 'Vision and Change')
    } else if(ass() == 'EcoEvo-MAPS') {
      scales <- list('Overall Scores', 'Vision and Change', 'Ecology and Evolution Core Concepts', 
                     '4DEE Framework')
    }
    updateSelectInput(session, "scale", label = "Scale:", choices = scales)
  })
  
  data.out <- reactive({
    if(compare.tab){
      if(input$match){
        Class1 <- subset(data(), Class_ID == levels(factor(data()$Class_ID))[1])
        Class2 <- subset(data(), Class_ID == levels(factor(data()$Class_ID))[2])
        matched.ID <- intersect(Class1$ID, Class2$ID)
        matched.FullName <- intersect(Class1$FullName, Class2$FullName)
        matched.BackName <- intersect(Class1$FullName, Class2$BackName)
        data.out <- subset(data(), ID %in% matched.ID | FullName %in% matched.FullName | 
                             FullName %in% matched.BackName)
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
    } else if((ass() == 'Phys-MAPS') & (input$scale != 'Vision and Change')){
      Scores.cols <- c('SC_Phys_Homeostasis', 'SC_Phys_CellCell_Communication', 
                       'SC_Phys_Flowdown_Gradients', 'SC_Phys_Cell_Membrane', 
                       'SC_Phys_Interdependence', 'SC_Phys_Structure_Function', 'SC_Phys_Evolution', 
                       'SC_Total_Score')
      Labels <- c('Homeostasis', 'Cell-cell communication', 'Flow-down gradients', 'Cell membrane',
                  'Interdependence', 'Structure/function', 'Evolution', 'Total Score')
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
    
    if(!is.null(class.var)) {
      Scores.cols <- c(Scores.cols, class.var)
      data.scale <- data.temp[, Scores.cols] %>%
        group_by_(class.var) %>%
        melt(.)
      p <- ggplot(data.scale, aes_string(x = 'variable', y = 'value', color = class.var))
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
  if(is.null(class.var)){
    return(reactive(input$demographic))
  } else if(compare.tab){
    return(data.out)
  }
}

ResponsesPlot <- function(input, output, session, data, ass, Demographic = NULL, class.var = NULL){
  observe({
    if(ass() == 'GenBio-MAPS'){
      questions <- list('01', '02', '03', '04', '07', '08', '12', '13', '14', '15', '16', '18',
                        '19', '20', '21', '22', '23', '24', '27', '28', '30', '31', '32', '33',
                        '35', '36', '37', '38', '40', '43', '44', '45', '49', '50', '54', '55',
                        '59', '60', '61')
    } else if(ass() == 'Phys-MAPS'){
      questions <- list('B', 'C', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'V', 'W', 'Z')
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
               class.var) %>%
        group_by_(class.var) %>%
        summarize_all(funs(mean), na.rm = TRUE) %>%
        melt(.)
      return(Responses.df)
    })
    output$plotResponses = renderPlot({
      p <- ggplot(Responses.df(), aes_string(x = 'variable', y = 'value', fill = class.var)) +
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
  for(Option in c('SexGender', 'URMStatus', 'ParentEducation', 'ClassStanding', 'Major', 
                  'TransferStatus', 'ELL')){
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