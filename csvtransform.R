setwd("~Desktop")
dat = read.csv("sample_nytimes16years.csv", stringsAsFactors=FALSE)

#convert stuff
dat[dat$X4 == -1, ]$X5 = ""
dat[dat$X4 == -1, ]$X6 = ""
dat[dat$X4 == -1, ]$X8 = ""
dat[dat$X4 == -1, ]$X10 = ""
dat[dat$X4 == -1, ]$X12 = ""
dat[dat$X4 == -1, ]$X4 = ""
write.csv(dat, file = "SampleData.csv")

#convert to utf-8 encoding
rty = file("sample_nytimes16years.csv",encoding="UTF-8")
write.csv("sample_nytimes16years.csv", file = rty)
