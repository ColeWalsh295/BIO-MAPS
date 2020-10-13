# Module server functions
# corresponding UI functions use the same function name with 'UI' appended to the end

DownloadClassData <- function(input, output, session, data, header, cols, ass, 
                              ClassID = NULL) {
  # retrieves relevant class data based on user input and provides downloadable data to
  # write to .csv
  
  observe({
    # I'm sure there is a better way to do this, but I gave up and this works to change
    # the popvers on the radio buttons based on selected assessment...its just Capstone
    # that's different
    if(ass() == 'GenBio-MAPS'){
      RadioPopover(ass())
    } else if(ass() == 'EcoEvo-MAPS'){
      RadioPopover(ass())
    } else if(ass() == 'Phys-MAPS'){
      RadioPopover(ass())
    } else if(ass() == 'Capstone'){
      RadioPopover(ass())
    }
  })
  observe({
    if(!is.null(ClassID)){
      updateTextInput(session, 'classID', value = ClassID())
    }
  })
  
  toListen <- reactive({
    list(input$classID, ass())
  })
  
  data.class <- eventReactive(toListen(), {
    # fixed bug where app would crash if instructors typed out ID rather than copying and
    # pasting...or if they just messed up
    validate(
      need(input$classID %in% data()$Class_ID, 'Enter a valid class ID')
    )
    data.class <- subset(data(), Class_ID == input$classID)
    return(data.class)
  })
  
  data.out <- reactive({
    # drop.cols <- c('Class_ID', 'Class_Level', 'FullName', 'BackName', 'ClassStanding',
    #                'TransferStatus', 'Major', 'SexGender', 'URMStatus', 'ELL', 
    #                'ParentEducation') # instructors can't download demographics
    # data.out <- data.class()[!(names(data.class()) %in% drop.cols)]
    data.out <- rbind(header()[, cols(), with = FALSE], data.class()[, cols(), 
                                                                     with = FALSE])
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
  
  return(data.class)
}

ClassStatistics <- function(input, output, session, data, Overall = FALSE){
  # computes and returns summary statistics for a set of data
  
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
                    summarize(Avg = round(mean(SC_Total_Score, na.rm = TRUE), 
                                          3) * 100) %>%
                    pull(), '%'),
            icon = icon("list"), color = "orange")
  })
  
  if(Overall){
    return(data.out) # we use the subsetted national dataset in the main server function
  }
}

ScalePlot <- function(input, output, session, data, ass, class.var = NULL,
                      compare.tab = FALSE){
  
  # plot box plots of students' scores on different dimensions
  
  observe({
    if(ass() == 'GenBio-MAPS'){
      scales <- list('Total scores & subdisciplines', 'Core concepts')
    } else if(ass() == 'Phys-MAPS'){
      scales <- list('Total scores & core principles', 'Core concepts')
    } else if(ass() == 'EcoEvo-MAPS'){
      scales <- list('Total scores & subdisciplines', 'Core concepts', 
                     'Ecology and evolution core concepts', '4DEE framework')
    } else if(ass() == 'Capstone'){
      scales <- list('Total scores & core concepts')
    }
    updateSelectInput(session, "scale", label = "Question Categorization:", 
                      choices = scales)
  })
  
  data.out <- reactive({
    if(compare.tab){
      if(input$match){
        Class1 <- subset(data(), Class_ID == levels(factor(data()$Class_ID))[1])
        Class2 <- subset(data(), Class_ID == levels(factor(data()$Class_ID))[2])
        matched.ID <- intersect(Class1$ID, Class2$ID)
        matched.FullName <- intersect(Class1$FullName, Class2$FullName)
        matched.BackName <- intersect(Class1$FullName, Class2$BackName)
        # match on ID, full name, and backwards full name...we pull out all the stops
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
    if((ass() == 'GenBio-MAPS') & (input$scale != 'Core concepts')) {
      Scores.cols <- c('SC_T_Cellular_and_Molecular', 'SC_T_Physiology', 
                       'SC_T_Ecology_and_Evolution', 'SC_Total_Score')
      Labels <- c('Cellular and Molecular', 'Physiology', 'Ecology and Evolution', 
                  'Total Score')
    } else if((ass() == 'Phys-MAPS') & (input$scale != 'Core concepts')){
      Scores.cols <- c('SC_Phys_Homeostasis', 'SC_Phys_CellCell_Communication', 
                       'SC_Phys_Flowdown_Gradients', 'SC_Phys_Cell_Membrane', 
                       'SC_Phys_Interdependence', 'SC_Phys_Structure_Function', 
                       'SC_Phys_Evolution', 'SC_Total_Score')
      Labels <- c('Homeostasis', 'Cell-cell communication', 'Flow-down gradients', 
                  'Cell membrane', 'Interdependence', 'Structure/function', 'Evolution', 
                  'Total Score')
    } else if((ass() == 'EcoEvo-MAPS') & (input$scale != 'Core concepts')) {
      if(input$scale == 'Total scores & subdisciplines') {
        Scores.cols <- c('SC_T_Ecology', 'SC_T_Evolution', 'SC_Total_Score')
        Labels <- c('Ecology', 'Evolution', 'Total Score')
      } else if(input$scale == 'Ecology and evolution core concepts') {
        Scores.cols <- c('SC_EE_Heritable_Variation', 'SC_EE_Modes_of_Change',
                         'SC_EE_Phylogeny_and_Evolutionary_History', 
                         'SC_EE_Biological_Diversity', 'SC_EE_Populations', 
                         'SC_EE_Energy_and_Matter', 'SC_EE_Interactions_with_Ecosystems', 
                         'SC_EE_Human_Impact')
        Labels <- c('Heritable\nVariation', 'Modes of\nChange', 
                    'Phylogeny and\nEvolutionary History', 'Biological\nDiversity', 
                    'Populations', 'Energy\nand Matter', 'Interactions\nwith Ecosystems', 
                    'Human\nImpact')
      } else if(input$scale == '4DEE framework') {
        Scores.cols <- c('SC_FDEE_Populations', 'SC_FDEE_Communities', 
                         'SC_FDEE_Ecosystems', 'SC_FDEE_Biomes', 'SC_FDEE_Biosphere', 
                         'SC_FDEE_Quantitative_Reasoning', 
                         'SC_FDEE_Designing_and_Critiquing', 'SC_FDEE_Human_Change',
                         'SC_FDEE_Human_Shape', 'SC_FDEE_Matter_and_Energy', 
                         'SC_FDEE_Systems', 'SC_FDEE_Space_and_Time')
        Labels <- c('Populations', 'Communities', 'Ecosystems', 'Biomes', 'Biosphere', 
                    'Quantitative reasoning\nand computational thinking', 
                    'Designing and\ncritiquing investigations', 
                    'Human accelerated\nenvironmental change',
                    'Humans shape resources\n/ecosystems/environment', 
                    'Transformations of\nenergy and matter', 'Systems', 'Space\nand Time')
      }
    } else if(ass() == 'Capstone'){
      Scores.cols <- c('SC_Total_Score', 'SC_VC_Evolution', 'SC_VC_Information_Flow', 
                       'SC_VC_Structure_Function', 
                       'SC_VC_Transformations_of_Energy_and_Matter', 'SC_VC_Systems')
      Labels <- c('Total Score', 'Evolution', 'Information Flow', 'Structure/Function',
                  'Transformations of\nEnergy and Matter', 'Systems')
    }
    else {
      Scores.cols <- c('SC_VC_Evolution', 'SC_VC_Information_Flow', 
                       'SC_VC_Structure_Function', 
                       'SC_VC_Transformations_of_Energy_and_Matter', 'SC_VC_Systems')
      Labels <- c('Evolution', 'Information Flow', 'Structure/Function',
                  'Transformations of\nEnergy and Matter', 'Systems')
    }
    
    if(!is.null(class.var)) {
      Scores.cols <- c(Scores.cols, class.var)
      data.scale <- data.temp[, Scores.cols] %>%
        group_by_(class.var) %>%
        melt(.)
      p <- ggplot(data.scale, aes_string(x = 'variable', y = 'value', color = class.var)) +
        scale_color_manual(values = c("#0072b2", "#d55e00", "#009e73", "#cc79a7"))
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
        data.count <- data.temp[data.temp[, Demographic()] != '', Scores.cols] %>%
          group_by_(Demographic()) %>%
          summarize(N = n())
        p <- ggplot(data.scale, aes_string(x = 'variable', y = 'value', color = Demographic())) +
          labs(color = input$demographic) +
          scale_color_manual(labels = paste(as.data.frame(data.count[, Demographic()])[, Demographic()], 
                                            ' (N = ', data.count$N, ')'),
                               values = c("#0072b2", "#d55e00", "#009e73", "#cc79a7"))
      }
    }
    if(length(Labels) > 7){ # things get squished when there are a lot of dimensions...
      p <- p + geom_boxplot(lwd = 1, position = position_dodge2(reverse = TRUE)) +
        coord_flip()
    } else {
      p <- p + geom_boxplot(lwd = 1)
    }
    p <- p + labs(x = input$scale, y = 'Score', title = "Your students' performance") +
      scale_x_discrete(labels = Labels) +
      shiny_theme +
      theme(legend.title = element_blank())
    return(p)
  })
  if(is.null(class.var)){
    return(reactive(input$demographic))
  } else if(compare.tab){
    return(data.out)
  }
}

ResponsesPlot <- function(input, output, session, data, ass, Demographic = NULL, 
                          class.var = NULL){
  # make bar plots of fraction of students getting each question correct
  
  observe({
    if(ass() == 'GenBio-MAPS'){
      questions <- list('01', '02', '03', '04', '07', '08', '12', '13', '14', '15', '16', 
                        '18', '19', '20', '21', '22', '23', '24', '27', '28', '30', '31', 
                        '32', '33', '35', '36', '37', '38', '40', '43', '44', '45', '49', 
                        '50', '54', '55', '59', '60', '61')
    } else if(ass() == 'Phys-MAPS'){
      questions <- list('B', 'C', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'V', 'W', 'Z')
    } else if(ass() == 'EcoEvo-MAPS') {
      questions <- list('Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9')
    } else if(ass() == 'Capstone'){
      questions <- list('Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10', 
                        'Q11', 'Q12', 'Q13', 'Q14', 'Q15', 'Q16', 'Q17', 'Q18')
    }
    updateSelectInput(session, "question", label = "Question:", choices = questions)
  })
  
  if(!is.null(Demographic)){
    Responses.df <- reactive({
      if(Demographic() == 'None'){
        Responses.df <- data() %>%
          select(c(grep(paste('^[^T]*', input$question, '_[0-9]*$', sep = ''), 
                        names(.)))) %>%
          summarize_all(funs(mean), na.rm = TRUE) %>%
          melt(.)
      } else {
        Responses.df <- data() %>%
          select(c(grep(paste('^[^T]*', input$question, '_[0-9]*$', sep = ''), names(.))), 
                 Demographic()) %>%
          group_by_(Demographic()) %>%
          summarize_all(funs(mean), na.rm = TRUE) %>%
          melt(.)
        Responses.df <- Responses.df[(Responses.df[, Demographic()] != '') & 
                                       !is.na(Responses.df[, Demographic()]),]
      }
      return(Responses.df)
    })
    output$plotResponses = renderPlot({
      if(Demographic() != 'None'){
        data.count <- data()[data()[, Demographic()] != '', ] %>%
          group_by_(Demographic()) %>%
          summarize(N = n())
        p <- ggplot(Responses.df(), aes_string(x = 'variable', y = 'value', 
                                               fill = Demographic())) +
          scale_fill_manual(labels = paste(as.data.frame(data.count[, Demographic()])[, Demographic()], 
                                            ' (N = ', data.count$N, ')'),
                             values = c("#0072b2", "#d55e00", "#009e73", "#cc79a7"))
      } else {
        p <- ggplot(Responses.df(), aes(x = variable, y = value))
      }
      p <- p + geom_bar(stat = 'identity', position =  position_dodge2(reverse = TRUE)) +
        coord_flip() +
        labs(x = 'Statement', y = 'Fraction of Correct Selections', 
             title = "Your students' performance by statement") +
        shiny_theme  +
        theme(legend.title = element_blank())

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
      p <- ggplot(Responses.df(), aes_string(x = 'variable', y = 'value', 
                                             fill = class.var)) +
        geom_bar(stat = 'identity', position = position_dodge2(reverse = TRUE)) +
        coord_flip() +
        labs(x = 'Statement', y = 'Fraction of Correct Selections', 
             title = "Your students' performance by statement") +
        scale_fill_manual(values = c("#0072b2", "#d55e00", "#009e73", "#cc79a7")) +
        shiny_theme  +
        theme(legend.title = element_blank())
      return(p)
    })
  }
}

DisableRadio <- function(df){
  # legacy; remove in future versions
  # disable particular radio buttons
  dataFrame <- reactive({
    dataFrame <- data.frame(df())
    return(dataFrame)
  })

  Titles = list('SexGender' = 'only male and female students are included',
                'URMStatus' = 'majority = white/asian; URM = all other students',
                'ParentEducation' = 'first generation student = neither parent graduated college',
                'ClassStanding' = 'freshman, sophomore/juniors, seniors, and grad students',
                'Major' = 'biology majors correspond to students planning to major in biology or any other life science',
                'TransferStatus' = 'transfer students include those who completed some college courses at another institution',
                'ELL' = 'students indicate whether their primary language growing up was english or another language')
  for(Option in c('SexGender', 'URMStatus', 'ParentEducation', 'ClassStanding', 'Major', 
                  'TransferStatus', 'ELL')){
    # availability columns labeled like x_Avail_Radio
    if(!dataFrame()[1, paste(Option, '_Avail_Radio', sep = '')]){
      shinyjs::runjs(paste("$('[type = radio][value = ", Option, "]').parent().parent().css('opacity', 0.4)", sep = ''))
      shinyjs::runjs(paste("$('[type = radio][value = ", Option, 
                           "]').prop('disabled', true)", sep = ''))
    } else {
      shinyjs::runjs(paste("$('[type = radio][value = ", Option, 
                           "]').parent().parent().css('opacity', 1)", sep = ''))
      shinyjs::runjs(paste("$('[type = radio][value = ", Option, "]').prop('disabled', false)", sep = ''))
      shinyjs::runjs(paste("$('[type = radio][value = ", Option, "]').closest('label').attr('title', '", Titles[[Option]], "')", sep = ''))
      }
  }
  return(0)  
}

RadioPopover <- function(assessment){
  Titles = list('SexGender' = 'only male and female students are included',
                'URMStatus' = 'majority = white/asian; URM = all other students',
                'ParentEducation' = 'first generation student = neither parent graduated college',
                'ClassStanding' = 'freshman, sophomore/juniors, seniors, and grad students',
                'Major' = 'biology majors correspond to students planning to major in biology or any other life science',
                'TransferStatus' = 'transfer students include those who completed some college courses at another institution',
                'ELL' = 'students indicate whether their primary language growing up was english or another language')
  for(Option in c('SexGender', 'URMStatus', 'ClassStanding')){
    shinyjs::runjs(paste("$('[type = radio][value = ", Option, "]').closest('label').attr('title', '", Titles[[Option]], "')", sep = ''))
  }
  if(assessment != 'Capstone'){
    for(Option in c('ParentEducation', 'Major', 'TransferStatus', 'ELL')){
    shinyjs::runjs(paste("$('[type = radio][value = ", Option, "]').parent().parent().css('opacity', 1)", sep = ''))
    shinyjs::runjs(paste("$('[type = radio][value = ", Option, "]').prop('disabled', false)", sep = ''))
    shinyjs::runjs(paste("$('[type = radio][value = ", Option, "]').closest('label').attr('title', '", Titles[[Option]], "')", sep = ''))
    
    }
  } else {
    # Capstone doesn't have these demographics available, so we disable and grey these radio
    # buttons to avoid confusion
    for(Option in c('ParentEducation', 'Major', 'TransferStatus', 'ELL')){
      shinyjs::runjs(paste("$('[type = radio][value = ", Option, "]').parent().parent().css('opacity', 0.4)", sep = ''))
      shinyjs::runjs(paste("$('[type = radio][value = ", Option, "]').prop('disabled', true)", sep = ''))
    }
  }
  return(0)  
}