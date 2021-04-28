library(tidyverse)
library(shiny)
library(shinyjs)
library(shinyalert)
shiny_theme <- theme_classic(base_size = 12)
library(shinydashboard)
library(shinyBS)
library(shinyhelper)
library(reshape2)
library(rsconnect)
library(plotly)
source('BioMAPS_Processing.R', local = TRUE)
source('BioMAPS_UI.R', local = TRUE)
source('BioMAPS_Server.R', local = TRUE)

GenBio <- Clean.GenBio()
GenBio.df <- GenBio$dataFrame
GenBio.header <- GenBio$header

EcoEvo <- Clean.EcoEvo()
EcoEvo.df <- EcoEvo$dataFrame
EcoEvo.header <- EcoEvo$header

Phys <- Clean.Phys()
Phys.df <- Phys$dataFrame
Phys.header <- Phys$header

Cap <- Clean.Cap()
Cap.df <- Cap$dataFrame
Cap.header <- Cap$header

### UI code ##############################################################################

### Your class tab ###

Your_tab = tabItem(
  tabName = "Your_Class",
  fluidRow(column(4, h2("View of your class") %>%
                    helper(icon = "question",
                           colour = "red",
                           type = "markdown",
                           content = "Your_tab"))),
  
  DownloadClassDataUI('Class.Main.Download', label = 'Your Class ID:', value = 'R_'),
  br(),
  ClassStatisticsOutput('Class.Main.Statistics'),
  br(),
  ScalePlotUI('Class.Main.Scale', Demos = TRUE),
  br(),br(),br(),br(),br(),br(), br(), br(), br(), br(), br(), br(),
  ResponsesPlotUI('Class.Main.Responses', Demos = TRUE)
)

### Compare two of your classes tab ###

Compare_tab = tabItem(
  tabName = "Compare_Classes",
  fluidRow(column(6, h2("Compare two of your classes") %>%
                    helper(icon = "question",
                           colour = "red",
                           type = "markdown",
                           content = "Compare_tab"))),
  
  DownloadClassDataUI('Class1.Download', label = 'Your first Class ID:',
                      value = 'R_'),
  br(),
  ClassStatisticsOutput('Class1.Statistics'),
  DownloadClassDataUI('Class2.Download', label = 'Your second Class ID:',
                      value = 'R_'),
  br(),
  ClassStatisticsOutput('Class2.Statistics'),
  ScalePlotUI('Class.Compare.Scale', Demos = FALSE, MatchBox = TRUE),
  br(), br(), br(), br(), br(),
  ResponsesPlotUI('Class.Compare.Responses', Demos = FALSE)
)

### Compare your class to national dataset tab ###

Overall_tab = tabItem(
  tabName = "Compare_Overall",
  fluidRow(column(7, h2("Compare your class to other classes") %>%
                    helper(icon = "question",
                           colour = "red",
                           type = "markdown",
                           content = "Aggregate_tab"))),
  
  DownloadClassDataUI('Class.You.Download', label = 'Your Class ID:',
                      value = 'R_'),
  br(),
  ClassStatisticsOutput('Class.You.Statistics'),
  br(),
  fluidRow(column(3, h3("Other classes") %>%
                    helper(icon = "question",
                           colour = "purple",
                           type = "markdown",
                           content = "OtherClasses"))),
  ClassStatisticsOutput('Class.Other.Statistics', Overall = TRUE),
  br(),
  ScalePlotUI('Overall.Compare.Scale', Demos = FALSE),
  br(), br(), br(), br(), br(),
  ResponsesPlotUI('Overall.Compare.Responses', Demos = FALSE)
)

### Server code ##########################################################################

server = function(input, output, session) {
  
  init.modal <- modalDialog(
    title = "How to use this dashboard",
    HTML('For more information about how to use this dashboard, click the "?" icons.<br><br>
      Note that data collected after 1 January 2021 will not be available on the data 
      explorer until June 2021.')
  )
  
  showModal(init.modal)
  
  observe_helpers(withMathJax = TRUE)
  
  df <- reactive({
    if(input$assessment == 'GenBio-MAPS'){
      df <- GenBio.df
    } else if(input$assessment == 'EcoEvo-MAPS'){
      df <- EcoEvo.df
    } else if(input$assessment == 'Phys-MAPS'){
      df <- Phys.df
    } else if(input$assessment == 'Capstone'){
      df <- Cap.df
    }
    return(df)
  })
  
  header.df <- reactive({
    if(input$assessment == 'GenBio-MAPS'){
      header.df <- GenBio.header
    } else if(input$assessment == 'EcoEvo-MAPS'){
      header.df <- EcoEvo.header
    } else if(input$assessment == 'Phys-MAPS'){
      header.df <- Phys.header
    } else if(input$assessment == 'Capstone'){
      header.df <- Cap.header
    }
    return(header.df)
  })
  
  cols <- reactive({
    # df has additional data that isn't needed for the app...get the intersection with the
    # headers containing relevant data columns
    cols <- intersect(colnames(header.df()), colnames(df()))
    return(cols)
  })
  
  Assessment <- reactive({
    # define this reactive variable to update arguments below along with df
    Assessment <- input$assessment
    return(Assessment)
  })
  
  ### Your Class tab ###
  
  CID <- NULL # set initial CID as null, update with input to retain CID between tabs
  df.Class <- callModule(DownloadClassData, 'Class.Main.Download', data = df, 
                         header = header.df, cols = cols, ass = Assessment, ClassID = CID)
  # Shiny update 1.5.0 introduced moduleServer, which can be used in lieu of callModule
  # for maintainability
  callModule(ClassStatistics, 'Class.Main.Statistics', data = df.Class)
  # set demographic as reactive to update two plots on this tab simultaneously with
  # demographic input
  demographic <- reactiveVal()
  demographic <- callModule(ScalePlot, 'Class.Main.Scale', data = df.Class, 
                            ass = Assessment)
  callModule(ResponsesPlot, 'Class.Main.Responses', data = df.Class, ass = Assessment, 
             Demographic = demographic)
  
  ### Compare Classes tab ###
  
  df.Class1 <- callModule(DownloadClassData, 'Class1.Download', data = df, 
                          header = header.df, cols = cols, ass = Assessment, ClassID = CID)
  callModule(ClassStatistics, 'Class1.Statistics', data = df.Class1)
  
  df.Class2 <- callModule(DownloadClassData, 'Class2.Download', data = df, 
                          header = header.df, cols = cols, ass = Assessment)
  callModule(ClassStatistics, 'Class2.Statistics', data = df.Class2)
  
  df.Compare <- reactive({
    rbind(df.Class1(), df.Class2())
  })
  
  df.Compare.match <- callModule(ScalePlot, 'Class.Compare.Scale', data = df.Compare, 
                                 ass = Assessment, class.var = 'Class_ID', 
                                 compare.tab = TRUE)
  callModule(ResponsesPlot, 'Class.Compare.Responses', data = df.Compare.match, 
             ass = Assessment, class.var = 'Class_ID')
  
  ### Compare your class to national dataset tab ###
  
  df.Class.You_temp <- callModule(DownloadClassData, 'Class.You.Download', data = df,
                    header = header.df, cols = cols, ass = Assessment, ClassID = CID)
  CID <- reactive({
    # update CID with input from each tab...this reactive variable ensures that text input
    # on one tab carries over to subsequent tabs so instructors don't have to re-type IDs
    if(input$tabs == 'Your_Class'){
      CID <- df.Class()$Class_ID[1]
    } else if(input$tabs == 'Compare_Classes'){
      CID <- df.Class1()$Class_ID[1]
    } else {
      CID <- df.Class.You_temp()$Class_ID[1]
    }
    return(CID)
  })
  callModule(ClassStatistics, 'Class.You.Statistics', data = df.Class.You_temp)
  
  df.Class.You <- reactive({
    df.Class.You <- df.Class.You_temp() %>%
      mutate(Class = 'Your Class') # add a column separating YOUR class from other classes
    return(df.Class.You)
  })
  df.Class.Other <- reactive({
    df.Class.Other <- df()[df()$Class_ID != df.Class.You_temp()$Class_ID[1],] %>%
      mutate(Class = 'Other Classes')
    return(df.Class.Other)
  })
  
  df.Other.filter <- callModule(ClassStatistics, 'Class.Other.Statistics', 
                                data = df.Class.Other, Overall = TRUE)
  
  df.Overall <- reactive({
    rbind(df.Class.You(), df.Other.filter())
  })
  callModule(ScalePlot, 'Overall.Compare.Scale', data = df.Overall, ass = Assessment,
             class.var = 'Class')
  callModule(ResponsesPlot, 'Overall.Compare.Responses', data = df.Overall, 
             ass = Assessment, class.var = 'Class')
}

##########################################################################################

dhead = dashboardHeader(title = h4(HTML("Bio-MAPS<br>Data Explorer")))

dside = dashboardSidebar(sidebarMenu(
  id = 'tabs',
  selectInput('assessment', "Assessment:", choices = c('GenBio-MAPS', 'EcoEvo-MAPS', 
                                                       'Phys-MAPS', 'Capstone')),
  menuItem("View of your class", tabName = "Your_Class", icon = icon("dashboard")),
  menuItem(HTML("Compare two of<br>your classes"), tabName = "Compare_Classes", 
           icon = icon("dashboard")),
  menuItem(HTML("Compare your class<br>to other classes"), tabName = "Compare_Overall", 
           icon = icon("dashboard"))
))

dbody = dashboardBody(
 tags$head(
   tags$link(rel = "stylesheet", type = "text/css", href = "Cornell.css")

 ),
 tabItems(Your_tab, Compare_tab, Overall_tab)
)

ui = tagList(useShinyjs(), useShinyalert(), dashboardPage(dhead, dside, dbody))

shinyApp(ui, server)