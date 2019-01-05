#####LIBRARIES######
if(!require(rstudioapi)) install.packages("rstudioapi")
if(!require(ggplot2)) install.packages("ggplot2")
if(!require(plotly)) install.packages("plotly")
if(!require(mice)) install.packages("mice")
if(!require(mclust)) install.packages("mclust") #Nice clustering library, guide: http://rstudio-pubs-static.s3.amazonaws.com/154174_78c021bc71ab42f8add0b2966938a3b8.html
if(!require(plyr)) install.packages("plyr") #"Library for the creation of the new variables."
if(!require(ggthemes))install.packages("ggthemes") # visualization
if(!require(scales))install.packages("scales") # visualization
if(!require(corrplot))install.packages("corrplot") # plots
if(!require(FactoMineR)) install.packages("fpc")
if(!require(cluster)) install.packages("cluster")
if(!require(mice)) install.packages("mice")
#import data
dades_train_P1 <- read.csv("~/Documents/Projects/Hacks/HackEPS/BonArea/dades_train_P2.csv")
#new parameter days difference
dades_train_P1$diffDate <- as.numeric(difftime(strptime(dades_train_P1$Dia_Servei, format = "%Y-%m-%d"),strptime(dades_train_P1$Dia_Comanda, format = "%Y-%m-%d"),units="days"))
# Detect outliers using robust mahalanobis distance and remove them
library(chemometrics)
library(mclust)
moutlier= Moutlier(X = dades_train_P1[-c(c(1:8),11,c(14:17),20)],quantile = 0.95)
outliers = sort(x = moutlier$rd,decreasing = TRUE, index.return=TRUE)
outlierstodelete = outliers$ix[1:3500] #DELETE 0.001% --> 30 INDIVIDUALS
dades_train_P1 = dades_train_P1[-outlierstodelete,]
#factor data
dades_train_P1$Dia_Comanda <- as.factor(dades_train_P1$Dia_Comanda)
dades_train_P1$Dia_Servei <- as.factor(dades_train_P1$Dia_Servei)
dades_train_P1$fuga <- as.factor(dades_train_P1$fuga)
dades_train_P1$Client <- as.factor(dades_train_P1$Client)
dades_train_P1$Poblacio <- as.factor(dades_train_P1$Poblacio)
dades_train_P1$Provincia <- as.factor(dades_train_P1$Provincia)




summary(dades_train_P1)
PCADefault = PCA(dades_train_P1[-c(c(1:8),11,c(14:17),20)],ncp = 10,graph = F)
contribution2 <- PCADefault$var$contrib

bestinfirstPCvar <- sort(contribution2[,1],decreasing = TRUE)[1:3] #Returns the variables that are more influencial(Contribution) in the first principal component
bestinfirstPCvar

bestinsecondPCvar <- sort(contribution2[,2],decreasing = TRUE)[1:3] #Returns the variables that are more influencial(contribution) in the second principal component
bestinsecondPCvar
#Significant dimensions
dim <- sum(as.numeric(PCADefault$eig[,3] <= 80))

#CLUSTERING

dim <- sum(as.numeric(PCADefault$eig[,3] <= 80))
Psi <- PCADefault$ind$coord[,1:dim]
centers = 20
defaultKmeans1 <- kmeans(Psi, centers =centers, iter.max = 50)
defaultKmeans2 <- kmeans(Psi, centers =centers, iter.max = 50)
table(defaultKmeans1$cluster,defaultKmeans2$cluster)
clas <- (defaultKmeans2$cluster-1)*centers+defaultKmeans1$cluster
freq <- table(clas)
freq
cdclas <- aggregate(as.data.frame(Psi),list(clas),mean)[,2:(dim+1)]
d2 <- dist(cdclas) #matrix of distances
h2 <- hclust(d2,method="ward.D2",members=freq) #Hiretical clustering, members = freq because not all the centroids have the same importance.
plot(h2)
barplot(h2$height[(nrow(cdclas)-40):(nrow(cdclas)-1)]) #Plot last 40 aggregations
nc = 2 # for instance, number of clusters.
c2 <- cutree(h2,nc)
cdg <- aggregate((diag(freq/sum(freq)) %*% as.matrix(cdclas)),list(c2),sum)[,2:(dim+1)] 
finalKmeans <- kmeans(Psi,centers=cdg)
Bss <- sum(rowSums(finalKmeans$centers^2)*finalKmeans$size)
Wss <- sum(finalKmeans$withinss)
Ib6 <- 100*Bss/(Bss+Wss)
Ib6
#Analysis of the clustering
finalKmeans$cluster <- as.factor(finalKmeans$cluster)
#How many individuals per cluster? 
#Needs interpretation depend of PCA...
finalKmeans$size
finalKmeans$cluster
dades_train_P1 <- cbind(dades_train_P1, clusterNum = finalKmeans$cluster)
Datacluste1 = dades_train_P1[dades_train_P1$clusterNum==1,]
sum(Datacluste1$fuga==1) 
summary(Datacluste1)
Datacluster2 = dades_train_P1[dades_train_P1$clusterNum==2,]
summary(Datacluster2)
sum(Datacluster2$fuga==1) 
clusplot(Psi, finalKmeans$cluster, color=TRUE, shade=TRUE, 
         labels=2, lines=0)

