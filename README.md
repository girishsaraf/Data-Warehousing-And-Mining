# Data-Warehousing-And-Mining
# Abstract for Credit Card Fraud detection
Credit card fraud is a wide-ranging term for theft and fraud committed using or involving a payment card, such as a credit card or debit card, as a fraudulent source of funds in a transaction. The purpose may be to obtain goods without paying, or to obtain unauthorized funds from an account. Credit card fraud is also an adjunct to identity theft. According to the United States Federal Trade Commission, while the rate of identity theft had been holding steady during the mid-2000s, it increased by 21 percent in 2008. However, credit card fraud, that crime which most people associate with ID theft, decreased as a percentage of all ID theft complaints for the sixth year in a row. Although incidences of credit card fraud are limited to about 0.1% of all card transactions, they have resulted in huge financial losses as the fraudulent transactions have been large value transactions. In 1999, out of 12 billion transactions made annually, approximately 10 million—or one out of every 1200 transactions—turned out to be fraudulent.
# Problem Definition
Credit Card Fraud costs banks millions of dollars a year in reimbursement, legal fees, and mitigation. Denying fraudulent transactions before they occur would greatly reduce expenses. In this project, we use a publically available dataset of 6.3 million credit card transactions and each is categorized as Fraud or Not Fraud. The result variable is Categorical & Binary.  False-positives are a major concern since we will deny any transactions that are flagged fraudulent forcing the customer to call customer service to complete the transaction. I test each model against 100,000 random transactions categorized as Not Fraud to estimate the false-positive rate.
# Data pre-processing
Dataset Preview
 
# Processing the Data Attributes value by value:

The attributes Step, Type, Amount, OldBalanceOrg, NewBalanceOrg, OldDest, NewDest, isFraud are important attributes. The isFlaggedFraud attribute is a result of some previous applied algorithm, hence the attribute can be deleted. The nameOrig also does not have any patterns and thus we can delete that as well. The nameDest attribute has two prefixes ‘C’ and ‘M’. Thus, we try to find any pattern specific to the prefixes. We convert the ‘isFraud’ attribute values to ‘Yes’ and ‘No’. We also convert the ‘type’ attribute into categorical since there are only 3 types of transactions. We also fnd that the ‘isFraud’ attribute has the value ‘Yes’ only in 8213 cases and these are only when the nameDest attribute has the prefix ‘C’. 
We also filter based on the type of transactions since the specific types of transactions only return the value for Fraud. We also remove the values above which transactions are not fraud (Max Transaction value). Since there are 8213 rows with the value of Fraud we generate 8213 random rows with the value of Fraud to be false. We also shuffle these rows according to step and setup the dataset so that the new dataset has all mixed values.
	Then we eliminate the highly correlated features as it may affect the efficiency of the overall model. Correlated features in general don't improve models (although it depends on the specifics of the problem like the number of variables and the degree of correlation), but they affect specific models in different ways and to varying extents. For linear models, multicollinearity can yield solutions that are wildly varying and possibly numerically unstable. Random forests can be good at detecting interactions between different features, but highly correlated features can mask these interactions. Support Vector machines can be affected when the features included are highly correlated. Then we divide the newly generated dataset into train, test and validate sets in order to implement the model of SVM and check the results generated.
# Algorithm Used
# Support Vector Machine:
In machine learning, support vector machines (SVMs, also support vector networks) are supervised  learning models with associated learning algorithms that analyze data used for classification and regression analysis. 
Given a set of training examples, each marked as belonging to one or the other of two categories, an SVM training algorithm builds a model that assigns new examples to one category or the other, making it a non-probabilistic binary linear classifier (although methods such as Platt scaling exist to use SVM in a probabilistic classification setting). An SVM model is a representation of the examples as points in space, mapped so that the examples of the separate categories are divided by a clear gap that is as wide as possible. New examples are then mapped into that same space and predicted to belong to a category based on which side of the gap they fall.

The pattern followed while testing the SVM model is:

1. fit the model to the data

2. Compare model against the data it was trained on

3. Compare model against the test dataset that was unknown for model building

4. Compare model against a 100k sample of Not Fraud cases to determine the expected false-positives.

In each of the models we will also track the time to create the model.

# Code Snippet:
  
# Results achieved
The SVM model implemented gave an output efficiency of about 94% and the system ran on the model for a duration of about 30 minutes to give the results. The results can be better but the SVM has predicted results as per the model training parameters. We can increase the scope by implementing different models on the same preprocessed data but with a different algorithm. This can help us to compare the efficiency on a better scale by contrasting the multiple results obtained.
 
