library(tidyverse)
library(shiny)
library(shinyjs)
library(shinyalert)
shiny_theme <- theme_classic(base_size = 18)
library(shinydashboard)
library(shinyBS)
library(shinyhelper)
library(data.table)
library(reshape2)
library(rsconnect)
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

server = function(input, output, session) {
  
  init.modal <- modalDialog(
    title = "How to use this dashboard",
    'For more information about how to use this dashboard, click the "?" icons.'
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
    cols <- intersect(colnames(header.df()), colnames(df()))
    return(cols)
  })
  
  Assessment <- reactive({
    Assessment <- input$assessment
    return(Assessment)
  })
  
  ### Your Class ###
  CID <- NULL
  df.Class <- callModule(DownloadClassData, 'Class.Main.Download', data = df, header = header.df, 
                      cols = cols, ass = Assessment, ClassID = CID)
  callModule(ClassStatistics, 'Class.Main.Statistics', data = df.Class)
  demographic <- reactiveVal()
  demographic <- callModule(ScalePlot, 'Class.Main.Scale', data = df.Class, ass = Assessment)
  callModule(ResponsesPlot, 'Class.Main.Responses', data = df.Class, ass = Assessment, 
             Demographic = demographic)
  
  ### Compare Classes ###
  df.Class1 <- callModule(DownloadClassData, 'Class1.Download', data = df, header = header.df, 
                          cols = cols, ass = Assessment, ClassID = CID)
  callModule(ClassStatistics, 'Class1.Statistics', data = df.Class1)
  
  df.Class2 <- callModule(DownloadClassData, 'Class2.Download', data = df, header = header.df, 
                          cols = cols, ass = Assessment)
  callModule(ClassStatistics, 'Class2.Statistics', data = df.Class2)
  
  df.Compare <- reactive({
    rbind(df.Class1(), df.Class2())
  })
  
  df.Compare.match <- callModule(ScalePlot, 'Class.Compare.Scale', data = df.Compare, 
                                 ass = Assessment, class.var = 'Class_ID', compare.tab = TRUE)
  callModule(ResponsesPlot, 'Class.Compare.Responses', data = df.Compare.match, ass = Assessment, 
             class.var = 'Class_ID')
  
  ### Compare to overall PLIC dataset ###
  
  df.Class.You_temp <- callModule(DownloadClassData, 'Class.You.Download', data = df,
                    header = header.df, cols = cols, ass = Assessment, ClassID = CID)
  CID <- reactive({
    if(input$tabs == 'Your_Class'){
      CID <- df.Class()[1, 'Class_ID']
    } else if(input$tabs == 'Compare_Classes'){
      CID <- df.Class1()[1, 'Class_ID']
    } else {
      CID <- df.Class.You_temp()[1, 'Class_ID']
    }
    return(CID)
  })
  callModule(ClassStatistics, 'Class.You.Statistics', data = df.Class.You_temp)
  
  df.Class.You <- reactive({
    df.Class.You <- df.Class.You_temp() %>%
      mutate(Class = 'Your Class')
    return(df.Class.You)
  })
  df.Class.Other <- reactive({
    df.Class.Other <- df()[df()$Class_ID != df.Class.You_temp()$Class_ID[1],] %>%
      mutate(Class = 'Other Classes')
    return(df.Class.Other)
  })
  
  df.Other.filter <- callModule(ClassStatistics, 'Class.Other.Statistics', data = df.Class.Other, Overall = TRUE)
  
  df.Overall <- reactive({
    rbind(df.Class.You(), df.Other.filter())
  })
  callModule(ScalePlot, 'Overall.Compare.Scale', data = df.Overall, ass = Assessment,
             class.var = 'Class')
  callModule(ResponsesPlot, 'Overall.Compare.Responses', data = df.Overall, ass = Assessment,
             class.var = 'Class')
}

# Set up the Header of the dashboard
dhead = dashboardHeader(title = h4(HTML("Bio-MAPS<br>Data Explorer")))

# Set up the sidebar which links to two pages
dside = dashboardSidebar(sidebarMenu(
  id = 'tabs',
  selectInput('assessment', "Assessment:", choices = c('GenBio-MAPS', 'EcoEvo-MAPS', 
                                                       'Phys-MAPS', 'Capstone')),
  menuItem("View of your class", tabName = "Your_Class", icon = icon("dashboard")),
  menuItem(HTML("Compare two of<br>your classes"), tabName = "Compare_Classes", icon = icon("dashboard")),
  menuItem(HTML("Compare your class<br>to other classes"), tabName = "Compare_Overall", 
           icon = icon("dashboard"))
))

# Here we set up the body of the dashboard

dbody = dashboardBody(
 tags$head(
   tags$link(rel = "stylesheet", type = "text/css",
             href = "Cornell.css")

 ),
 tabItems(Your_tab, Compare_tab, Overall_tab)
)

# Combining header, sidebar, and body
ui = tagList(useShinyjs(), useShinyalert(), dashboardPage(dhead, dside, dbody))#, 
             #tags$script(HTML("$(document).ready(function(){$('[data-toggle='popover']').popover();});")))

# Generating a local instance of your dashboard
shinyApp(ui, server)