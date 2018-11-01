#   Libraries need to be run for the code to run
#   Link for Dataset: https://www.kaggle.com/ntnu-testimon/paysim1
#   Dataset size is approx 400+ MB
#   Dataset on kaggle
#   Code has both data preprocessing and machine development lines.

library(plyr)
library(tidyverse)
library(caret)
library(GGally)
library(stringr)
library(rattle)
library(pROC)
library(ROCR)

#read data
set.seed(317)
fraud_raw <- read_csv("PS_20174392719_1491204439457_log.csv")
glimpse(fraud_raw)

fraud_df <- fraud_raw %>%
  mutate(name_orig_first = str_sub(nameOrig,1,1)) %>%
  mutate(name_dest_first = str_sub(nameDest, 1, 1)) %>%
  select(-nameOrig, -nameDest)

#nameDest
unique(fraud_df$name_dest_first)
fraud_df$name_dest_first <- as.factor(fraud_df$name_dest_first)
table(fraud_df$name_dest_first)

#nameOrig
unique(fraud_df$name_orig_first)
fraud_df2 <- fraud_df %>%
  select(-name_orig_first, -isFlaggedFraud) %>%
  select(isFraud, type, step, everything())

glimpse(fraud_df2)

fraud_df2$type <- as.factor(fraud_df2$type)
fraud_df2$isFraud <- as.factor(fraud_df2$isFraud)
fraud_df2$isFraud <- recode_factor(fraud_df2$isFraud, `0` = "No", `1` = "Yes")

summary(fraud_df2)

#fraud transactions
fraud_trans <- fraud_df2 %>%
  filter(isFraud == "Yes") 
summary(fraud_trans)

#reducing dataset
fraud_df3 <- fraud_df2 %>%
  filter(type %in% c("CASH_OUT", "TRANSFER")) %>%
  filter(name_dest_first == "C") %>%
  filter(amount <= 10000000) %>%
  select(-name_dest_first)
summary(fraud_df3)

#sample dataset
not_fraud <- fraud_df3 %>%
  filter(isFraud == "No") %>%
  sample_n(8213)

is_fraud <- fraud_df3 %>%
  filter(isFraud == "Yes")

full_sample <- rbind(not_fraud, is_fraud) %>%
  arrange(step)
#graphs
ggplot(full_sample, aes(x = step, col = isFraud)) + 
  geom_histogram(bins = 743)
#only fraud
ggplot(is_fraud, aes(x = step)) + 
  geom_histogram(bins = 743)

ggpairs(full_sample)

summary(full_sample)

#preprocessing
preproc_model <- preProcess(fraud_df3[, -1], 
                            method = c("center", "scale", "nzv"))

fraud_preproc <- predict(preproc_model, newdata = fraud_df3[, -1])

fraud_pp_w_result <- cbind(isFraud = fraud_df3$isFraud, fraud_preproc)

summary(fraud_pp_w_result)

#high correlational
fraud_numeric <- fraud_pp_w_result %>%
  select(-isFraud, -type)
high_cor_cols <- findCorrelation(cor(fraud_numeric), cutoff = .75, verbose = TRUE, 
                                 names = TRUE, exact = TRUE)
high_cor_removed <- fraud_pp_w_result %>%
  select(-newbalanceDest)

fraud_numeric <- high_cor_removed %>%
  select(-isFraud, -type)
comboInfo <- findLinearCombos(fraud_numeric)
comboInfo

#modelling
model_df <-high_cor_removed
is_fraud <- model_df %>%
  filter(isFraud == "Yes")

not_fraud <- model_df %>%
  filter(isFraud == "No") %>%
  sample_n(8213)

# To mix up the sample set I'll arrange by `step`
model_full_sample <- rbind(is_fraud, not_fraud) %>%
  arrange(step)
#splitting
in_train <- createDataPartition(y = model_full_sample$isFraud, p = .75, 
                                list = FALSE) 
train <- model_full_sample[in_train, ] 
test <- model_full_sample[-in_train, ] 

gc()

control <- trainControl(method = "repeatedcv", 
                        number = 10, 
                        repeats = 3, 
                        classProbs = TRUE, 
                        summaryFunction = twoClassSummary)

big_no_sample <- model_df %>%
  filter(isFraud == "No") %>%
  sample_n(100000)

#svm
start_time <- Sys.time()
svm_model <- train(isFraud ~ ., 
                   data = train, 
                   method = "svmRadial",   # Radial kernel
                   tuneLength = 3,  # 3 values of the cost function
                   metric="ROC",
                   trControl=control)
end_time <- Sys.time()
end_time - start_time

print(svm_model$finalModel)

#prediction on training set
svm_train_pred <- predict(svm_model, train)
confusionMatrix(train$isFraud, svm_train_pred, positive = "Yes")

#prediction on test set
svm_test_pred <- predict(svm_model, test)
confusionMatrix(test$isFraud, svm_test_pred, positive = "Yes")

#predict on no-fraud dataset
start_time <- Sys.time()
svm_big_no_pred <- predict(svm_model, big_no_sample)
end_time <- Sys.time()
end_time - start_time

confusionMatrix(big_no_sample$isFraud, svm_big_no_pred, positive = "Yes")
#ROC
svm_probs <- predict(svm_model, test, type = "prob")
svm_ROC <- roc(response = test$isFraud, 
               predictor = svm_probs$Yes, 
               levels = levels(test$isFraud))

plot(svm_ROC, col = "black")
#area under curve
auc(svm_ROC)
