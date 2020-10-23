

# Libraries
library(readxl)
library(dplyr)
library(stringr)
library(writexl)
# Path

path<-"J:/articulos/articulos/anuncios y género/EPH"
setwd(path)



# Load data
data<-read_xlsx("usu_individual_T120.xlsx")
CNO<-read_xlsx("CNO_codigos.xlsx")

# Cleaning a bit
data<-data[data$P21>0,]


# Checking data
# Income
data$P21
# Occupation category

#Clasificador de Actividades
# Económicas para Encuestas
# Sociodemográficas del Mercosur, CAES-
# Mercosur
data$PP04B_COD 

# CNO 2001
unique(data$PP04D_COD)
# Adding zeros to compare with the CNO code
# The loop below check for NA, if not NA then continue
# Add N "0" based on digits
data$PP04D_COD2<- -1
for (row in 1:length(data$PP04D_COD) ){
  if (is.na(data[row,]$PP04D_COD)){
  next} else{
    N<-5-str_count(data[row,]$PP04D_COD, pattern = "")
    if(N==0){
      data[row,]$PP04D_COD2<- data[row,]$PP04D_COD
    } else if(N==1){
      data[row,]$PP04D_COD2<-as.numeric(paste(data[row,]$PP04D_COD,"0",sep = "", collapse = NULL))
    } else if(N==2){
      data[row,]$PP04D_COD2<-as.numeric(paste(data[row,]$PP04D_COD,"00",sep = "", collapse = NULL))
    } else if (N==3){
      data[row,]$PP04D_COD2<-as.numeric(paste(data[row,]$PP04D_COD,"000",sep = "", collapse = NULL))
    } else if (N==4){
      data[row,]$PP04D_COD2<-as.numeric(paste(data[row,]$PP04D_COD,"0000",sep = "", collapse = NULL))
    }
  }
}

# Checking
test <- data.frame("PP04D_COD" = data$PP04D_COD, 
                  "PP04D_COD2" = data$PP04D_COD2) 
unique(data$PP04D_COD)
unique(data$PP04D_COD2)

# Getting means, median, std...
results1<-data %>%  group_by(PP04D_COD2)%>% 
  summarise(Mean=mean(P21), Max=max(P21), Min=min(P21), 
            Median=median(P21))#, Std=sd(P21)
results2<-data %>%  group_by(PP04B_COD)%>% 
   summarise(Mean=mean(P21), Max=max(P21), Min=min(P21), 
             Median=median(P21))#, Std=sd(P21)



# Working with CNO
CNO$digit2<-substr(CNO$`Código CNO-01`, start = 1, stop = 2)
CNO$digit3<-substr(CNO$`Código CNO-01`, start = 4, stop = 4)
CNO$digit4<-substr(CNO$`Código CNO-01`, start = 6, stop = 6)
CNO$digit5<-substr(CNO$`Código CNO-01`, start = 8, stop = 8)
# Removing dots, we use \\ to recognize dots, then replace with nothing ("")
CNO$code<-gsub("\\.", "", CNO$`Código CNO-01`)

# New dataframe to merge with results
CNO_code_desc <- data.frame("code" = CNO$code, 
                   "desc" = CNO$`Descripción CNO-01`) 

# Merging results
results1<-merge(results1, CNO_code_desc, by.x="PP04D_COD2", by.y="code")

write_xlsx(results1,"resultadosCNO.xlsx")













###################### OLD CODE


data$PP04D_COD2<-NA
for (row in 1:length(data$PP04D_COD) ){
  if (is.na(data[row,]$PP04D_COD)){
    print("hola")} else{print("chau")
    }}




data$PP04D_COD2<-paste(data$PP04D_COD, ,sep = "", collapse = NULL)
as.character(data$PP04D_COD) as.character("0")
unique(data$PP04D_COD2)


