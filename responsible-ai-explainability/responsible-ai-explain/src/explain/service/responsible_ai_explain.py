'''
Copyright 2024-2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), 
to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies 
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE 
AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import warnings
warnings.filterwarnings('ignore')
import asyncio
import os
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]="0"

from alibi.explainers import AnchorText, AnchorTabular, PartialDependenceVariance, PermutationImportance, IntegratedGradients
from alibi.explainers import TreeShap, KernelShap
from lime.lime_tabular import LimeTabularExplainer
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from keras.utils import pad_sequences
from explain.constants.local_constants import *
from explain.config.logger import CustomLogger
import pandas as pd
import numpy as np
import requests
import json
import shap

log = CustomLogger()

class ResponsibleAIExplain:

    def split_set(X, y, fraction, random_state=0):
        """
        Given a set X, associated labels y, splits a fraction y from X.
        """
        _, X_split, _, y_split = train_test_split(X,
                                                  y,
                                                  test_size=fraction,
                                                  random_state=random_state,
                                                  )
        log.info(f"Number of records: {X_split.shape[0]}")
        log.info(f"Number of class {0}: {len(y_split) - y_split.sum()}")
        log.info(f"Number of class {1}: {y_split.sum()}")

        return X_split, y_split
    
    def prepare_data(dataset, targetClassLabel, targetClassNames=None):
        """
        Prepares the data and target from the dataset.

        Parameters:
        dataset (DataFrame): The dataset to be prepared.
        targetClassLabel (str): The label of the target class.
        targetClassNames (list, optional): The names of the target classes.

        Returns:
        data, target, featureNames, targetClassNames: The data and target arrays, feature names, and target class names.
        """
        # Check if targetClassLabel is in dataset
        if targetClassLabel in dataset.columns:
            # Prepare the data and target
            data = dataset.drop(targetClassLabel, axis=1, inplace=False)
            target = dataset[targetClassLabel]
        else:
            data = dataset
            target = None

        # Get the feature names
        featureNames = data.columns.to_list()

        # If targetClassNames is not provided, get the unique values from the target
        if targetClassNames is None and target is not None:
            targetClassNames = target.unique()

        # Convert data to numpy array
        data = data.values

        # Convert target to numpy array if it is not None
        if target is not None:
            target = target.values

        return data, target, featureNames, targetClassNames
    
    def pipeline_processing(pipeline, dataset, targetClassLabel, inputData=None):
        """
        Given a pipeline (which includes preprocessing steps and a model) and a dataset, 
        this function preprocesses the dataset, optionally encodes categorical target class labels, 
        and returns the extracted model from the pipeline, transformed dataset, the preprocessed class label and optionally the transformed input data if provided.

        Parameters:
        pipeline : A list where the last element is expected to be a tuple containing the model and its preprocessor.
        dataset (DataFrame): The dataset to be preprocessed, expected to be a pandas DataFrame.
        targetClassLabel (str): The name of the column in the preprcessed dataset that contains the target class labels.
        inputData (DataFrame, optional): The input data to be transformed using the preprocessor.

        Returns:
        model, transformed_dataset, preprocessed_class_label, transformed_input_data : The extracted model from the pipeline, the dataset after applying preprocessing, the preprocessed class label, and optionally the transformed input data if provided.
        """
        # Initialize variables
        transformed_data = None
        preprocessed_class_label = None
        preprocessor_features_count = 0

        # Extract the model and preprocessor from the pipeline
        model = pipeline.steps[-1][1]
        preprocessor = pipeline[:-1]
        dataset_columns_count = len(dataset.columns)

        # Check if the preprocessor has a feature count attribute
        if hasattr(preprocessor, 'n_features_in_'):
            preprocessor_features_count = preprocessor.n_features_in_

        if inputData is not None:
            inputData = pd.DataFrame(preprocessor.transform(inputData), columns=preprocessor.get_feature_names_out())

        #  Check dataset columns count and preprocessor features count
        if dataset_columns_count-1 == preprocessor_features_count:
            preprocessed_class_label = targetClassLabel
            # Extract the features from the dataset except the target class label
            features = dataset.drop(targetClassLabel, axis=1)
            # Transform the features using the preprocessor
            transformed_data= pd.DataFrame(preprocessor.transform(features))
            
            categorical_features = dataset.select_dtypes(include=['object', 'category']).columns.tolist()
            # Check if the target class label is categorical
            if targetClassLabel in categorical_features:
                # Encode the target class labels
                ordinal_encoder = preprocessing.OrdinalEncoder()
                transformed_data[targetClassLabel] = ordinal_encoder.fit_transform(dataset[[targetClassLabel]]).astype(int)
            else:
                # Copy the target class labels as is
                transformed_data[targetClassLabel] = dataset[targetClassLabel]
        # Check if the dataset columns count is equal to the preprocessor features count
        elif dataset_columns_count == preprocessor_features_count:
            # Transform the dataset using the preprocessor
            transformed_data = pd.DataFrame(preprocessor.transform(dataset))
            # Check if the target class label is present in the transformed data
            for i in transformed_data.columns:
                if targetClassLabel in str(i):
                    preprocessed_class_label= str(i)
                    break

        preprocessed_feature_names = preprocessor.get_feature_names_out()
        # Check if the dataset columns count is not equal to the preprocessor features count
        if dataset_columns_count != len(preprocessed_feature_names):
            # Append the target class label to the preprocessed feature names
            preprocessed_feature_names = np.append(preprocessed_feature_names, targetClassLabel)
        # Create a DataFrame from the transformed data
        preprocessed_data = pd.DataFrame(transformed_data.values, columns=preprocessed_feature_names)

        # Return the model, preprocessed data, and preprocessed class label
        return model, preprocessed_data, preprocessed_class_label, inputData
    
    def find_date_column(dataset):
        for column in dataset.columns:
            try:
                # Attempt to convert the column to datetime
                temp_series = pd.to_datetime(dataset[column], errors='coerce')
                # Check if most of the column could be converted successfully
                if not temp_series.isna().mean() > 0.5:  # Arbitrary threshold, adjust based on your data
                    return column
            except Exception as e:
                # If any error occurs during conversion, move to the next column
                continue
        # If no date column is found, raise an exception
        raise ValueError("No date/datetime format column found in the dataset.")


    def hlstr(string, color='white', size='18px', font='sans-serif'):
        """
        Return HTML markup highlighting text with the desired color.
        """
        return f"<mark style='background-color:{color}; font-size:{size}; font-family:{font};'>{string} </mark>"
    
    def colorize(attrs, cmap='PiYG'):
        """
        Compute hex colors based on the attributions for a single instance.
        Uses a diverging colorscale by default and normalizes and scales
        the colormap so that colors are consistent with the attributions.
        """
        import matplotlib as mpl
        cmap_bound = np.abs(attrs).max()
        norm = mpl.colors.Normalize(vmin=-cmap_bound, vmax=cmap_bound)
        cmap = mpl.cm.get_cmap(cmap)

        # now compute hex values of colors
        colors = list(map(lambda x: mpl.colors.rgb2hex(cmap(norm(x))), attrs))
        return colors
    
    def endpoint_check(x):
        if x.shape[0]==1:
            response = requests.post(url, json={input_request: x.reshape(1, -1).tolist()})
        else:
            response = requests.post(url, json={input_request: x.tolist()})
        prediction = json.loads(response.text)[output_response]
        
        return np.array(prediction)
        
    def anchor_tabular_local_explanation(params: dict):
        # Log the start of the explanation process
        log.info("Running Local Explanation for Structured Tabular Data using Anchor Tabular")
        
        try:
            global url, input_request, output_response
            
            # Extract necessary information from params
            model = params['model']
            dataset = params['dataset']
            modelType = params['modelType']
            targetClassLabel = params['targetClassLabel']
            targetClassNames = params['targetClassNames']
            inputData = params['lineDataset']
            inputIndex = params['inputIndex']
            input_request = params['api_input_request']
            output_response = params['api_output_response']
            modelName = type(model).__name__

            # Check if the model is a pipeline
            if modelName =='Pipeline':
                model, dataset, targetClassLabel, inputData = ResponsibleAIExplain.pipeline_processing(model, dataset, targetClassLabel, inputData)

            # Check if the input index is valid
            if inputIndex < 0 or inputIndex >= len(dataset):
                raise ValueError("Input index must be between 0 and the length of the dataset.")

            # Define the prediction function based on the model type
            if modelType != 'API' and modelType is not None:
                predict_fn = lambda x: model.predict(x)
            elif modelType == 'API' and modelType is not None:
                url = model
                predict_fn = ResponsibleAIExplain.endpoint_check

            # Prepare the data and target
            data, target, featureNames, targetClassNames = ResponsibleAIExplain.prepare_data(dataset, targetClassLabel, targetClassNames)

            # Initialize the explainer
            explainer = AnchorTabular(predictor=predict_fn, feature_names=featureNames)

            # Fit the explainer
            explainer.fit(data)
            
            inp_data = inputData.values if inputData is not None else data[:500]

            result = []
            
            # Define a function to generate the explanation for each row in the DataFrame
            def explanation(inp_data):

                # Generate the explanation
                explaination = explainer.explain(np.array(inp_data), verbose_every=0)
                
                # Create a list of dictionaries directly from the data and feature names
                inputRow = [{"featureName": key, "featureValue": val} for key, val in zip(featureNames, inp_data.tolist())]

                # Make a prediction using the explainer's predictor
                prediction = targetClassNames[int(explainer.predictor(inp_data.to_numpy().reshape(1, -1))[0])]

                result.append({"inputRow": inputRow,
                               "modelPrediction": str(prediction),
                               "explanation": explaination.anchor})

            # Apply the function to each row in the DataFrame
            pd.DataFrame(inp_data).apply(explanation, axis=1)
            
            # Return the predicted target, anchor, and input row
            return [{"anchor": result,
                     "description": ANCHOR_TABULAR_DES}]

        except Exception as e:
            # Log the error and return an empty result
            log.error(e, exc_info=True)
            raise
        
    def kernel_shap_local_explanation(params: dict):
        # Log the start of the explanation process
        log.info("Running Local Explanation for Structured Tabular Data using Kernel Shap")
        
        try:
            global url, input_request, output_response

            # Extract the parameters
            model = params['model']
            taskType = params['taskType']
            modelType = params['modelType']
            dataset = params['dataset']
            targetClassLabel = params['targetClassLabel']
            targetClassNames = params['targetClassNames']
            inputIndex = params['inputIndex']
            inputData = params['lineDataset']
            input_request = params['api_input_request']
            output_response = params['api_output_response']
            modelName = type(model).__name__

            # Check if the model is a pipeline
            if modelName =='Pipeline':
                model, dataset, targetClassLabel, inputData = ResponsibleAIExplain.pipeline_processing(model, dataset, targetClassLabel, inputData)

            # Check if the input index is valid
            if inputIndex < 0 or inputIndex >= len(dataset):
                raise ValueError("Input index must be between 0 and the length of the dataset.")
            
            # Define the prediction function based on the model type
            if modelType != 'API':
                predict_fn = lambda x: model.predict(x)
            else:
                url = model
                predict_fn = ResponsibleAIExplain.endpoint_check

            # Prepare the data and target
            data, target, featureNames, targetClassNames = ResponsibleAIExplain.prepare_data(dataset, targetClassLabel, targetClassNames)

            # Initialize the explainer
            if taskType == 'REGRESSION':
                explainer = KernelShap(predict_fn, task='regression', feature_names=featureNames)
                
            elif taskType == 'CLASSIFICATION':
                explainer = KernelShap(predict_fn, feature_names=featureNames)
            
            # Check the size of the dataset
            if len(data) < 2:
                # If the dataset has less than 2 samples, it's too small to fit the explainer
                raise ValueError("Dataset is too small to fit the explainer. Please provide dataset with more samples.")
            elif len(data) > 100:
                # If the dataset has more than 100 samples, we only take the first 100 samples for efficiency
                train_data = data[:100]
            else:
                train_data = data
            
            # Fit the explainer
            explainer.fit(train_data)
            
            inp_data = inputData.values if inputData is not None else data[:500]
            result = []
            
            def explanation(data):
                # Generate the explanation
                explanation = explainer.explain(np.array([data]))

                # Extract feature importances from the explanation
                importances = explanation['data']['raw']['importances']

                # Initialize lists for storing feature importances and kernel SHAP values
                list_importance, sorted_data = [], {}
                
                # Iterate over the items in the importances dictionary
                for feature, importance in importances.items():
                    # Skip irrelevant features for regression tasks
                    if taskType == "REGRESSION" and feature == 'aggregated':
                        continue
                    # Skip irrelevant features for non-regression tasks
                    elif taskType != "REGRESSION" and feature != str(explanation['raw']['prediction'][0]):
                        continue

                    # Create a dictionary mapping feature names to their ranked effect
                    data_dict = dict(zip(importance['names'], importance['ranked_effect']))

                    # Sort the data by ranked effect in descending order
                    sorted_data = dict(sorted(data_dict.items(), key=lambda x: x[1], reverse=True))

                # Create a list of dictionaries directly from the data and feature names
                inputRow = [{"featureName": key, "featureValue": val} for key, val in zip(featureNames, data.tolist())]

                # Normalize the feature importances to a scale from 1 to 100
                original_list = list(sorted_data.values())
                min_val, max_val = min(original_list), max(original_list)
                normalized_list = [1 + 99 * (x - min_val) / (max_val - min_val) for x in original_list]

                # Scale the normalized importances so that they sum to 100
                scaling_factor = 100 / sum(normalized_list)
                new_normalized_list = [x * scaling_factor for x in normalized_list]

                # Create a list of dictionaries of feature names and their normalized importances
                list_importance = [{"featureName": k, "importanceScore": round(v, 4)} for k, v in zip(sorted_data.keys(), new_normalized_list)][:10]
                
                # Prepare the output based on the task type
                if modelType != "Keras":
                    predictedTarget = str(explanation['raw']['raw_prediction'][0]) if taskType == 'REGRESSION' else str(targetClassNames[explanation['raw']['raw_prediction'][0]])
                else:
                    predictedTarget = str(targetClassNames[int(np.argmax(explanation['raw']['raw_prediction'][0]))])
                
                result.append({"inputRow": inputRow,
                               "modelPrediction": predictedTarget,
                               "explanation": list_importance})

            # Apply the function to each row in the DataFrame
            pd.DataFrame(inp_data).apply(explanation, axis=1)
            
            return [{"importantFeatures": result,
                     "description":LOCAL_KERNEL_SHAP_DES}]
        
        except Exception as e:
            # Log the error and return an empty result
            log.error(e, exc_info=True)
            raise
        
    def kernel_shap_global_explanation(params: dict):
        # Log the start of the explanation process
        log.info("Running Global Explanation for Structured Tabular Data using Kernel Shap")
        
        try:
            global url,input_request,output_response
            
            # Extract necessary information from params
            model = params['model']
            taskType = params['taskType']
            modelType = params['modelType']
            dataset = params['dataset']
            targetClassLabel = params['targetClassLabel']
            targetClassNames = params['targetClassNames']
            input_request = params['api_input_request']
            output_response = params['api_output_response']
            modelName = type(model).__name__

            # Check if the model is a pipeline
            if modelName =='Pipeline':
                model, dataset, targetClassLabel, inputData = ResponsibleAIExplain.pipeline_processing(model, dataset, targetClassLabel)

            # Define the prediction function based on the model type
            if modelType != 'API':
                predict_fn = lambda x: model.predict(x)
            else:
                url = model
                predict_fn = ResponsibleAIExplain.endpoint_check

            # Prepare the data and target
            data, target, featureNames, targetClassNames = ResponsibleAIExplain.prepare_data(dataset, targetClassLabel, targetClassNames)

            # Initialize the explainer
            if taskType == 'REGRESSION':
                explainer = KernelShap(predict_fn, task='regression', feature_names=featureNames)
                
            elif taskType == 'CLASSIFICATION':
                explainer = KernelShap(predict_fn, feature_names=featureNames)
            
            elif taskType == 'CLUSTERING':
                # Train a decision tree on the data
                tree = DecisionTreeClassifier(max_depth=3)
                predictions = predict_fn(data)

                new_model = tree.fit(data, predictions)
                new_predict_fn = lambda x: new_model.predict(x)
                
                explainer = KernelShap(new_predict_fn, feature_names=featureNames)

            
            # Check the size of the dataset
            if len(data) < 2:
                # If the dataset has less than 2 samples, it's too small to fit the explainer
                raise ValueError("Dataset is too small to fit the explainer. Please provide dataset with more samples.")
            elif len(data) > 100:
                # If the dataset has more than 100 samples, we only take the first 100 samples for efficiency
                data = data[:100]
            
            # Fit the explainer
            explainer.fit(data)
            
            # Generate the explanation
            explanation = explainer.explain(data, featureNames=featureNames)

            # Extract feature importances from the explanation
            importances = explanation['data']['raw']['importances']

            # Initialize list for storing kernel SHAP values
            list_kernel_shap = []

            # Iterate over the items in the importances dictionary
            for item in importances.items():
                # Skip irrelevant features
                if item[0] == 'aggregated':
                    break

                # Create a dictionary mapping feature names to their ranked effect
                sorted_data = dict(sorted(zip(item[1]['names'], item[1]['ranked_effect']), key=lambda x: x[1], reverse=True))

                # Normalize the feature importances to a scale from 1 to 100
                original_list = list(sorted_data.values())
                min_val, max_val = min(original_list), max(original_list)
                normalized_list = [1 + 99 * (x - min_val) / (max_val - min_val) for x in original_list]

                # Scale the normalized importances so that they sum to 100
                scaling_factor = 100 / sum(normalized_list)
                new_normalized_list = [x * scaling_factor for x in normalized_list]

                # Define the threshold
                threshold = 5

                # Create a list of dictionaries of feature names and their normalized importances
                list_importance = [{"featureName": k, "importanceScore": round(v, 4)} for k, v in zip(sorted_data.keys(), new_normalized_list)]

                # Separate features based on the threshold
                important_features = [feature for feature in list_importance if feature['importanceScore'] >= threshold]
                other_features = [feature for feature in list_importance if feature['importanceScore'] < threshold]

                # Calculate the total importance score for 'Others'
                others_importance_score = sum(feature['importanceScore'] for feature in other_features)

                important_features.append({"featureName": "Others", "importanceScore": round(others_importance_score, 4)})

                # Append the list of important features to the list_kernel_shap list
                list_kernel_shap.append({"inputRow": None,
                                         "modelPrediction": None, 
                                         "explanation": important_features})
                break 
            
            return [{'importantFeatures': list_kernel_shap, 'featureNames': featureNames, 'description': GLOBAL_KERNEL_SHAP_DES}]
            
        except Exception as e:
            # Log the error and return an empty result
            log.error(e, exc_info=True)
            raise

    def timeSeries_global_explanation(params: dict):
        # Log the start of the explanation process
        log.info("Running Global Explanation for Structured Tabular Data using Kernel Explainer")
        try:
            global topFeatureNames
            # Extract necessary information from params
            model = params['model']
            dataset = params['dataset']
            targetClassLabel = params['targetClassLabel']
            targetClassNames = params['targetClassNames']
            modelType =  params['modelType']

            # Prepare the data and target
            data, target, featureNames, targetClassNames = ResponsibleAIExplain.prepare_data(dataset, targetClassLabel, targetClassNames)
            
            if modelType != 'Scikit-learn':
                date_column_name = ResponsibleAIExplain.find_date_column(dataset)
                dataset.set_index(date_column_name, inplace=True)
                featureNames = dataset.columns.to_list()
                featureNames.remove(targetClassLabel)
                exog = dataset[featureNames].head(100)
                # Use 50 rows for the background dataset for the explainer
                background_exog = dataset[featureNames].head(50)
                def predict_arimax(exog_data):
                    # Ensure the exogenous data has the same structure as the training data
                    exog_data = pd.DataFrame(exog_data, columns=featureNames)
                    predictions = model.get_forecast(steps=len(exog_data), exog=exog_data).predicted_mean
                    return predictions.values

                explainer = shap.KernelExplainer(predict_arimax, background_exog)
                instance = exog
            else:
                explainer = shap.KernelExplainer(model.predict, data[:100])
                # Select the instances to explain (can also randomize this selection)
                instance = data[:100]

            # Compute SHAP values for the selected instance
            shap_values = explainer.shap_values(instance)

            # Aggregate SHAP values to get feature importances
            feature_importances = np.abs(shap_values).mean(axis=0).flatten()
            # Convert to list
            feature_importances_list = feature_importances.tolist()
            # Normalize the feature importances to a scale from 1 to 100
            min_val, max_val = min(feature_importances_list), max(feature_importances_list)
            normalized_importances = [1 + 99 * (x - min_val) / (max_val - min_val) for x in feature_importances]

            # Scale the normalized importances so that they sum to 100
            scaling_factor = 100 / sum(normalized_importances)
            new_normalized_importances = [x * scaling_factor for x in normalized_importances]
            # Create a list of dictionaries of feature names and their normalized importances
            list_importance = [{"featureName": k, "importanceScore": round(v, 4)} for k, v in zip(featureNames, new_normalized_importances)]

            # Sort the list by importanceScore in descending order
            sorted_list_importance = sorted(list_importance, key=lambda x: x["importanceScore"], reverse=True)

            # Extract the top 10 feature names based on importance
            topFeatureNames = [item["featureName"] for item in sorted_list_importance[:10]]

            # Define the threshold
            threshold = 5

            # Separate features based on the threshold
            important_features = [feature for feature in sorted_list_importance if feature['importanceScore'] >= threshold]
            other_features = [feature for feature in sorted_list_importance if feature['importanceScore'] < threshold]

            # Calculate the total importance score for 'Others'
            others_importance_score = sum(feature['importanceScore'] for feature in other_features)

            important_features.append({"featureName": "Others", "importanceScore": round(others_importance_score, 4)})
            list_time_series = []
           
            # Append the list of important features to the list_kernel_shap list
            list_time_series.append({"inputRow": None,
                                    "modelPrediction": None, 
                                    "explanation": important_features})
               
            return [{"timeSeries":list_time_series,
                     "featureNames":featureNames,
                     "description":LOCAL_TS_LIME_EXPLAINER_DES}] 
        except Exception as e:
            # Log the error and re-raise the exception
            log.error(e, exc_info=True)
            raise

    def timeSeries_local_explanation_lime(params: dict):
        # Log the start of the explanation process
        log.info("Running Local Explanation for Structured Tabular Data using Lime Tabular")
        try:
            global url, topFeatureNames
            
            # Extract necessary information from params
            model = params['model']
            taskType = params['taskType']
            modelType = params['modelType']
            dataset = params['dataset']
            targetClassLabel = params['targetClassLabel']
            targetClassNames = params['targetClassNames']
            inputData = params['lineDataset']
            inputIndex = params['inputIndex']
            modelName = type(model).__name__

             # Check if the model is a pipeline
            if modelName =='Pipeline':
                model, dataset, targetClassLabel, inputData = ResponsibleAIExplain.pipeline_processing(model, dataset, targetClassLabel, inputData)

            # Check if the input index is valid
            if inputIndex < 0 or inputIndex >= len(dataset):
                raise ValueError("Input index must be between 0 and the length of the dataset.")

            # Prepare the data and target
            data, target, featureNames, targetClassNames = ResponsibleAIExplain.prepare_data(dataset, targetClassLabel, targetClassNames)

            if modelType != 'Scikit-learn':
                date_column_name = ResponsibleAIExplain.find_date_column(dataset)
                dataset.set_index(date_column_name, inplace=True)
                featureNames = dataset.columns.to_list()
                featureNames.remove(targetClassLabel)
                endog = dataset[targetClassLabel]
                exog = dataset[featureNames]
                data = exog
                def predict_arimax(exog_data):
                    # Ensure the exogenous data has the same structure as the training data
                    exog_data = pd.DataFrame(exog_data, columns=featureNames)
                    predictions = model.get_forecast(steps=len(exog_data), exog=exog_data).predicted_mean
                    
                    return predictions.values
                # Initialize the forecasting model
                explainer = LimeTabularExplainer(exog.values, mode="regression", training_labels=endog, feature_names=featureNames)

            else:
                # Initialize the forecasting model
                explainer = LimeTabularExplainer(data, feature_names=featureNames, mode='regression')

            inp_data = inputData.values if inputData is not None else data[:500]
            result = []
            
            def explanation(data):
                if modelType != 'Scikit-learn':
                    # Generate the explanation
                    explanation = explainer.explain_instance(data, predict_arimax, num_features=len(featureNames))
                else:
                    # Generate the explanation
                    explanation = explainer.explain_instance(data, model.predict, num_features=len(featureNames))
                prediction = round(explanation.predicted_value, 5)
                data_dict = dict(explanation.as_list())
                # Sort the data by importance values in descending order
                sorted_data = dict(sorted(data_dict.items(), key=lambda x: abs(x[1]), reverse=True))
                # Normalize the absolute importance values to a scale from 1 to 100
                original_list = list(sorted_data.values())

                abs_list = [abs(x) for x in original_list]
               
                min_val, max_val = min(abs_list), max(abs_list)
               
                if max_val == min_val:
                    normalized_list = [1 for _ in abs_list]
                else:
                    normalized_list = [1 + 99 * (x - min_val) / (max_val - min_val) for x in abs_list]

                # # Reapply the original signs to the normalized values
                signed_normalized_list = [x if original >= 0 else -x for x, original in zip(normalized_list, original_list)]

                # # Scale the normalized importances so that they sum to 100
                scaling_factor = 100 / sum(abs(x) for x in signed_normalized_list)
                new_normalized_list = [x * scaling_factor for x in signed_normalized_list]
                
                # Generate the list of importances using a list comprehension with scaled scores
                list_importance = [{"featureName": k, "importanceScore": round(v, 4)} for k, v in zip(sorted_data.keys(), new_normalized_list)][:10]
                
                data_df = pd.DataFrame([data])
                data_df.columns = featureNames
               
                filtered_data = data_df[topFeatureNames]

                # Create an input row from the DataFrame
                input_row = filtered_data.iloc[0]

                # Create the inputRow list of dictionaries
                inputRow = [{"featureName": key, "featureValue": val} for key, val in input_row.items()]
                
                result.append({"modelPrediction": str(prediction),
                                "explanation":list_importance,
                                "inputRow":inputRow})
                
            # Apply the function to each row in the DataFrame
            pd.DataFrame(inp_data).apply(explanation, axis=1)
            
            return [{"timeSeries": result,
                     "featureNames": featureNames,
                     "description": LIME_TABULAR_DES}]

        except Exception as e:
            # Log the error and return an empty result
            log.error(e, exc_info=True)
            raise
        
    def tree_shap_local_explanation(params: dict):
        # Log the start of the explanation process
        log.info("Running Local Explanation for Structured Tabular Data using Tree Shap")
        
        try:
            global url
            
            # Extract necessary information from params
            model = params['model']
            taskType = params['taskType']
            dataset = params['dataset']
            targetClassLabel = params['targetClassLabel']
            targetClassNames = params['targetClassNames']
            inputData = params['lineDataset']
            inputIndex = params['inputIndex']
            modelName = type(model).__name__

            # Check if the model is a pipeline
            if modelName =='Pipeline':
                model, dataset, targetClassLabel, inputData = ResponsibleAIExplain.pipeline_processing(model, dataset, targetClassLabel, inputData)

            #Check if the input index is valid
            if inputIndex < 0 or inputIndex >= len(dataset):
                raise ValueError("Input index must be between 0 and the length of the dataset.")

            # Prepare the data and target
            data, target, featureNames, targetClassNames = ResponsibleAIExplain.prepare_data(dataset, targetClassLabel, targetClassNames)

            # Initialize the explainer
            if taskType == 'REGRESSION':
                explainer = TreeShap(model, task='regression', feature_names=featureNames)
                
            elif taskType == 'CLASSIFICATION':
                explainer = TreeShap(model, feature_names=featureNames)

            # Fit the explainer
            explainer.fit()
            
            inp_data = inputData.values if inputData is not None else data[:500]
            result = []

            def explanation(data):

                # Generate the explanation 
                explanation = explainer.explain(np.array([data]), check_additivity=False)

                # Extract feature importances from the explanation
                importances = explanation['data']['raw']['importances']

                # Iterate over the items in the importances dictionary
                for item in importances.items():
                    
                    if modelName in ['XGBClassifier','GradientBoostingClassifier']:
                        # Prepare the predicted target based on the task type
                        predictedTarget = str(explanation['raw']['raw_prediction']) if taskType == 'REGRESSION' else str(targetClassNames[explanation['raw']['prediction']])
                        # Skip irrelevant features
                        if (taskType == "REGRESSION" and item[0] == 'aggregated') or (taskType != "REGRESSION" and item[0] != str(explanation['raw']['prediction']) and item[0] != 'aggregated'):
                            continue
                    else:
                        # Prepare the predicted target based on the task type
                        predictedTarget = str(explanation['raw']['raw_prediction']) if taskType == 'REGRESSION' else str(targetClassNames[explanation['raw']['prediction'][0]])
                        if (taskType == "REGRESSION" and item[0] == 'aggregated') or (taskType != "REGRESSION" and item[0] != str(explanation['raw']['prediction'][0])):
                            continue
                    
                    # Create a sorted dictionary of feature names and their ranked effects
                    sorted_data = dict(sorted(zip(item[1]['names'], item[1]['ranked_effect']), key=lambda x: x[1], reverse=True))
                
                # Create a list of dictionaries directly from the data and feature names
                inputRow = [{"featureName": key, "featureValue": val} for key, val in zip(featureNames, data.to_numpy().tolist())]

                # Normalize the feature importances to a scale from 1 to 100
                original_list = list(sorted_data.values())
                min_val, max_val = min(original_list), max(original_list)
                normalized_list = [1 + 99 * (x - min_val) / (max_val - min_val) for x in original_list]
                
                # Scale the normalized importances so that they sum to 100
                scaling_factor = 100 / sum(normalized_list)
                new_normalized_list = [x * scaling_factor for x in normalized_list]

                # Create a list of dictionaries of feature names and their normalized importances
                list_importance = [{"featureName": k, "importanceScore": round(v, 4)} for k, v in zip(sorted_data.keys(), new_normalized_list)]
                
                # Append the list of important features to the list_tree_shap list
                result.append({"inputRow": inputRow, 
                               "modelPrediction": predictedTarget, 
                               "explanation": list_importance})
            
            # Apply the function to each row in the DataFrame
            pd.DataFrame(inp_data).apply(explanation, axis=1)
            
            return [{"importantFeatures": result,
                    "description":LOCAL_TREE_SHAP_DES}]
        
        except Exception as e:
            # Log the error and return an empty result
            log.error(e, exc_info=True)
            raise
        
    def tree_shap_global_explanation(params: dict):
        log.info("Running Global Explanation for Structured Tabular Data using Tree Shap")
        try:
            # Extract necessary information from params
            model = params['model']
            taskType = params['taskType']
            dataset = params['dataset']
            targetClassLabel = params['targetClassLabel']
            targetClassNames = params['targetClassNames']
            modelName = type(model).__name__

            # Check if the model is a pipeline
            if modelName =='Pipeline':
                model, dataset, targetClassLabel, inputData = ResponsibleAIExplain.pipeline_processing(model, dataset, targetClassLabel)
            
            # Define the prediction function for the model
            predict_fn = lambda x: model.predict(x)

            # Prepare the data and target
            data, target, featureNames, targetClassNames = ResponsibleAIExplain.prepare_data(dataset, targetClassLabel, targetClassNames)

            # Initialize the explainer
            if taskType == 'REGRESSION':
                explainer = TreeShap(model, task='regression', feature_names=featureNames)
                
            elif taskType == 'CLASSIFICATION':
                explainer = TreeShap(model, feature_names=featureNames)
            
            elif taskType == 'CLUSTERING':
                tree = DecisionTreeClassifier(max_depth=3)
                predictions = predict_fn(data)
                
                new_model = tree.fit(data, predictions)
                
                explainer = TreeShap(new_model, feature_names=featureNames, categorical_names=targetClassNames)
            
            # Fit the explainer
            explainer.fit()

            # Check if the dataset is too large 
            if len(data) > 100:
                # If the dataset is too large, limit it to the first 100 samples
                data = data[:100]
            elif len(data) < 2:
                # If the dataset is too small, raise an error
                raise ValueError("Dataset is too small to fit the explainer. Please provide dataset with more samples.")
            
            # Generate the explanation for the first 100 samples
            explanation = explainer.explain(data)
            
            # Extract feature importances from the explanation
            feature_importances = explanation['data']['raw']['importances']

            # Initialize list for storing tree SHAP values
            shap_values, feature_importance_list = [], []
            
            idx = 0
            # Iterate over the items in the feature_importances dictionary
            for idx, (class_name, feature_importance) in enumerate(feature_importances.items()):
                # Skip irrelevant features
                if class_name == 'aggregated' and taskType == "REGRESSION":
                    continue
                if taskType == "CLASSIFICATION" and class_name != 'aggregated':
                    continue
                
                # Create a sorted dictionary of feature names and their ranked effects
                sorted_importances = dict(sorted(zip(feature_importance['names'], feature_importance['ranked_effect']), key=lambda x: x[1], reverse=True))
                
                # Normalize the feature importances to a scale from 1 to 100
                original_importances = list(sorted_importances.values())
                min_importance, max_importance = min(original_importances), max(original_importances)
                normalized_importances = [1 + 99 * (x - min_importance) / (max_importance - min_importance) for x in original_importances]

                # Scale the normalized importances so that they sum to 100
                scaling_factor = 100 / sum(normalized_importances)
                scaled_importances = [x * scaling_factor for x in normalized_importances]

                feature_importance_dict = []
                # Add the target class name to the feature importance dictionary
                if class_name == 'aggregated':
                    feature_importance_dict.append({"ClassName": "Overall aggregated feature importance"})
                else:
                    if isinstance(targetClassNames[idx], str):
                        feature_importance_dict.append({"ClassName": targetClassNames[idx]})
                    else:
                        feature_importance_dict.append({"ClassName": targetClassNames[idx].tolist()})

                # Create a list of dictionaries of feature names and their normalized importances
                feature_importance_values_dict = [{"featureName": name, "importanceScore": round(value, 4)} for name, value in zip(sorted_importances.keys(), scaled_importances)]

                feature_importance_dict[0]["importantFeatures"] = feature_importance_values_dict

                # Add the feature importance dictionary to the list
                feature_importance_list.append(feature_importance_dict[0])

            # Append the list of important features to the shap_values list
            shap_values.append({"inputRow": None,
                                "modelPrediction": None, 
                                "explanation": feature_importance_list})

            # Return the list of important features
            return [{'importantFeatures': shap_values, 'description': GLOBAL_TREE_SHAP_DES}]

        except Exception as e:
            log.error(f"Failed to generate global explanation: {str(e)}")
            raise
        
    def permutation_importance_global_explanation(params: dict):
        # Log the start of the explanation process
        log.info("Running Global Explanation for Structured Tabular Data using Permutation Importance")
        
        try:
            global url,input_request,output_response
            
            # Extract necessary information from params
            model = params['model']
            taskType = params['taskType']
            modelType = params['modelType']
            dataset = params['dataset']
            targetClassLabel = params['targetClassLabel']
            targetClassNames = params['targetClassNames']
            input_request = params['api_input_request']
            output_response = params['api_output_response'] 
            modelName = type(model).__name__

            # Check if the model is a pipeline
            if modelName =='Pipeline':
                model, dataset, targetClassLabel, inputData = ResponsibleAIExplain.pipeline_processing(model, dataset, targetClassLabel)

            # Define the prediction function based on the model type
            if modelType != 'API':
                predict_fn = lambda x: model.predict(x)
            else:
                url = model
                predict_fn = ResponsibleAIExplain.endpoint_check

            # Prepare the data and target
            data, target, featureNames, targetClassNames = ResponsibleAIExplain.prepare_data(dataset, targetClassLabel, targetClassNames)

            # Initialize the explainer
            if taskType == 'REGRESSION':
                explainer = PermutationImportance(predictor=predict_fn, loss_fns=['mean_absolute_error'], feature_names=featureNames)
                
            elif taskType == 'CLASSIFICATION':
                explainer = PermutationImportance(predictor=predict_fn, score_fns=['accuracy'], feature_names=featureNames)

            # Generate the explanation
            exp_importance = explainer.explain(X=data, y=target)

            # Extract feature importance values and create a dictionary with feature names
            feature_importance_values = [item['mean'] for item in exp_importance.feature_importance[0]]
            data = dict(zip(featureNames, feature_importance_values))

            # Sort the data by importance values in descending order
            sorted_data = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))

            # Normalize the importance values to a scale from 1 to 100
            original_list = list(sorted_data.values())
            min_val, max_val = min(original_list), max(original_list)
            normalized_list = [1 + 99 * (x - min_val) / (max_val - min_val) for x in original_list]

            # Scale the normalized importances so that they sum to 100
            scaling_factor = 100 / sum(normalized_list)
            new_normalized_list = [x * scaling_factor for x in normalized_list]

            # Create a list of dictionaries of feature names and their normalized importances
            list_data = [{"featureName": k, "importanceScore": round(v, 4)} for k, v in zip(sorted_data.keys(), new_normalized_list)]
            
            # Return the list of important features
            return [{'importantFeatures': [{"inputRow": None,
                                            "modelPrediction": None, 
                                            "explanation": list_data}],
                     "description": GLOBAL_PERMUTATION_IMPORTANCE_DES}]

        except Exception as e:
            # Log the error and return an empty result
            log.error(e, exc_info=True)
            raise
        
    def partial_dependence_variance_global_explanation(params: dict):
        # Log the start of the explanation process
        log.info("Running Global Explanation for Structured Tabular Data using Partial Dependence Variance")
        
        try:
            global url,input_request,output_response
            
            # Extract necessary information from params
            model = params['model']
            taskType = params['taskType']
            modelType = params['modelType']
            dataset = params['dataset']
            targetClassLabel = params['targetClassLabel']
            targetClassNames = params['targetClassNames']
            input_request = params['api_input_request']
            output_response = params['api_output_response']
            modelName = type(model).__name__

            # Check if the model is a pipeline
            if modelName =='Pipeline':
                model, dataset, targetClassLabel, inputData = ResponsibleAIExplain.pipeline_processing(model, dataset, targetClassLabel)

            # Define the prediction function based on the model type
            if modelType != 'API':
                # predict_fn = model.predict
                predict_fn = lambda x: model.predict(x)
            else:
                url = model
                predict_fn = ResponsibleAIExplain.endpoint_check

            # Prepare the data and target
            data, target, featureNames, targetClassNames = ResponsibleAIExplain.prepare_data(dataset, targetClassLabel, targetClassNames)

            # Initialize the explainer
            explainer = PartialDependenceVariance(predictor=predict_fn, 
                                                  target_names=targetClassNames, 
                                                  feature_names=featureNames
                                                  )
           
            # Generate the explanation
            exp_importance = explainer.explain(X=data, method='importance')
        
            # Create a dictionary with feature names and their importance values
            data = dict(zip(featureNames, exp_importance.feature_importance[0]))
            
            # Sort the data by importance values in descending order
            sorted_data = dict(sorted(data.items(), key = lambda x: x[1], reverse = True))

            # Normalize the importance values to a scale from 1 to 100
            original_list = list(sorted_data.values())
            min_val, max_val = min(original_list), max(original_list)
            normalized_list = [1 + 99 * (x - min_val) / (max_val - min_val) for x in original_list]

            # Scale the normalized importances so that they sum to 100
            scaling_factor = 100 / sum(normalized_list)
            new_normalized_list = [x * scaling_factor for x in normalized_list]

            # Create a list of dictionaries of feature names and their normalized importances
            list_data = [{"featureName": k, "importanceScore": round(v, 4)} for k, v in zip(sorted_data.keys(), new_normalized_list)]

            # Return the list of important features
            return [{'importantFeatures': [{"inputRow": None,
                                            "modelPrediction": None, 
                                            "explanation": list_data}],
                     "description": GLOBAL_PD_VARIANCE_DES}]
            
        except Exception as e:
            # Log the error and return an empty result
            log.error(e, exc_info=True)
            raise
    
    def lime_tabular_local_explanation(params: dict):
        # Log the start of the explanation process
        log.info("Running Local Explanation for Structured Tabular Data using Lime Tabular")
        
        try:
            global url
            
            # Extract necessary information from params
            model = params['model']
            taskType = params['taskType']
            modelType = params['modelType']
            dataset = params['dataset']
            targetClassLabel = params['targetClassLabel']
            targetClassNames = params['targetClassNames']
            inputData = params['lineDataset']
            inputIndex = params['inputIndex']
            modelName = type(model).__name__

             # Check if the model is a pipeline
            if modelName =='Pipeline':
                model, dataset, targetClassLabel, inputData = ResponsibleAIExplain.pipeline_processing(model, dataset, targetClassLabel, inputData)

            # Check if the input index is valid
            if inputIndex < 0 or inputIndex >= len(dataset):
                raise ValueError("Input index must be between 0 and the length of the dataset.")

            # Prepare the data and target
            data, target, featureNames, targetClassNames = ResponsibleAIExplain.prepare_data(dataset, targetClassLabel, targetClassNames)

            # Initialize the explainer
            if taskType == 'REGRESSION':
                explainer = LimeTabularExplainer(data, feature_names=featureNames, class_names=targetClassNames, mode='regression')
                
            elif taskType == 'CLASSIFICATION':
                explainer = LimeTabularExplainer(data, feature_names=featureNames, class_names=targetClassNames, mode='classification')

            inp_data = inputData.values if inputData is not None else data[:500]
            result = []
            
            def explanation(data):
                # Generate the explanation
                if taskType == 'REGRESSION':
                    explanation = explainer.explain_instance(data, model.predict)
                    prediction = round(explanation.predicted_value, 5)
                else:
                    if modelType != 'Keras':
                        explanation = explainer.explain_instance(data, model.predict_proba)
                        prediction = targetClassNames[model.predict([data])[0]]
                    else:
                        explanation = explainer.explain_instance(data, model.predict)
                        prediction = targetClassNames[int(np.argmax(model.predict([data])[0]))]
                
                data_dict = dict(explanation.as_list())
                # Sort the data by importance values in descending order
                sorted_data = dict(sorted(data_dict.items(), key=lambda x: abs(x[1]), reverse=True))
                # Normalize the absolute importance values to a scale from 1 to 100
                original_list = list(sorted_data.values())

                abs_list = [abs(x) for x in original_list]
               
                min_val, max_val = min(abs_list), max(abs_list)
               
                if max_val == min_val:
                    normalized_list = [1 for _ in abs_list]
                else:
                    normalized_list = [1 + 99 * (x - min_val) / (max_val - min_val) for x in abs_list]

                # Reapply the original signs to the normalized values
                signed_normalized_list = [x if original >= 0 else -x for x, original in zip(normalized_list, original_list)]

                # Scale the normalized importances so that they sum to 100
                scaling_factor = 100 / sum(abs(x) for x in signed_normalized_list)
                new_normalized_list = [x * scaling_factor for x in signed_normalized_list]
                
                # Generate the list of importances using a list comprehension with scaled scores
                list_importance = [{"featureName": k, "importanceScore": round(v, 4)} for k, v in zip(sorted_data.keys(), new_normalized_list)][:10]
               
                # Create a list of dictionaries directly from the data and feature names
                inputRow = [{"featureName": key, "featureValue": val} for key, val in zip(featureNames, data.to_numpy().tolist())][:10]
                
                result.append({"modelPrediction": str(prediction),
                                "explanation":list_importance,
                                "inputRow":inputRow})
                
            # Apply the function to each row in the DataFrame
            pd.DataFrame(inp_data).apply(explanation, axis=1)
            
            return [{"importantFeatures":result,
                     "featureNames": featureNames,
                     "description":LIME_TABULAR_DES}]

        except Exception as e:
            # Log the error and return an empty result
            log.error(e, exc_info=True)
            raise

    def text_shap_local_explanation(params: dict):
        # Log the start of the explanation process
        log.info("Running Local Explanation for Text Data using Shap")
        try:
            
            # Extract necessary information from params
            model = params['model']
            dataset = params['dataset']
            preprocessor = params['preprocessor']
            targetClassNames = params['targetClassNames']
            inputData = params['lineDataset']
        
            if preprocessor is not None:
                predict_fn = lambda x: model.predict(preprocessor.transform(x))
                transformed_data = preprocessor.transform(inputData if inputData is not None else dataset[:500])
            else:
                predict_fn = lambda x: model.predict(x)

            dataset = inputData if inputData is not None else dataset[:500]

            # Create a SHAP explainer
            explainer = shap.Explainer(model, transformed_data)

            result=[]
            
            def process_row(row):
                inputText = row  # assuming row is a text
                prediction = targetClassNames[predict_fn([inputText])[0]]
                
                # Get the feature names
                feature_names = preprocessor.get_feature_names_out()

                # Create a mask for features present in "good movie"
                input_vector = preprocessor.transform([inputText]).toarray()
                relevant_features = input_vector[0] > 0

                shap_values = explainer.shap_values(input_vector)

                # Create a mask to filter SHAP values and feature names
                filtered_shap_values = shap_values[:, relevant_features]
                filtered_feature_names = feature_names[relevant_features]

                filtered_shap_values = filtered_shap_values.flatten()

                # Convert SHAP values to a dictionary
                data_dict = dict(zip(filtered_feature_names, filtered_shap_values))

                # Sort the data by importance values in descending order
                sorted_data = dict(sorted(data_dict.items(), key=lambda x: abs(x[1]), reverse=True))

                # Normalize the absolute importance values to a scale from 1 to 100
                original_list = list(sorted_data.values())
                abs_list = [abs(x) for x in original_list]
                min_val, max_val = min(abs_list), max(abs_list)

                if max_val == min_val:
                    normalized_list = [1 for _ in abs_list]
                else:
                    normalized_list = [1 + 99 * (x - min_val) / (max_val - min_val) for x in abs_list]

                # Reapply the original signs to the normalized values
                signed_normalized_list = [x if original >= 0 else -x for x, original in zip(normalized_list, original_list)]

                # Scale the normalized importances so that they sum to 100
                scaling_factor = 100 / sum(abs(x) for x in signed_normalized_list)
                new_normalized_list = [x * scaling_factor for x in signed_normalized_list]

                # Create a list of dictionaries of feature names and their normalized importances
                list_importance = [{"featureName": k, "importanceScore": round(v, 4)} for k, v in zip(sorted_data.keys(), new_normalized_list)]
  
                result.append({"inputText": inputText, "modelPrediction":prediction,  "explanation":list_importance})
            
            # Apply the function to each row in the DataFrame
            dataset[dataset.columns[0]].apply(process_row)
            
            return [{"shapImportanceText": result, "featureNames" : None, "description": LOCAL_TS_LIME_EXPLAINER_DES}]

        except Exception as e:
            # Log the error and re-raise the exception
            log.error(e, exc_info=True)
            raise
        
    def anchor_text_local_explanation(params: dict):
        try:
            # Extract necessary information from params
            model = params['model']
            dataset = params['dataset']
            preprocessor = params['preprocessor']
            targetClassNames = params['targetClassNames']
            inputData = params['lineDataset']
        
            if preprocessor is not None:
                predict_fn = lambda x: model.predict(preprocessor.transform(x))
            else:
                predict_fn = lambda x: model.predict(x)

            explainer = AnchorText.load('../models//alibi//', predictor=predict_fn)
            result=[]
            
            def process_row(row):
                inputText = row  # assuming row is a text
                prediction = targetClassNames[predict_fn([inputText])[0]]
                
                explanation = explainer.explain(inputText,
                                                threshold=0.95,
                                                stop_on_first=True,
                                                min_samples_start=100,
                                                coverage_samples=100
                                                )
               
                if len(explanation.anchor) == 0 :
                    url = os.getenv("TOKEN_IMP_URL")
                    payload = {"inputPrompt": inputText, "modelName": "code" }
                    response = requests.request("POST", url, json=payload, verify=False).json()
                    exp = response['token_importance_mapping'][0]['token'].replace(' ', '')
                    if exp in inputText:
                        explanation.anchor = [word for word in inputText.split() if exp in word]

                # Check if explanation.anchor length is more than one and does not contain certain keywords
                modelConfidence = 'Low'
                if len(explanation.anchor) > 1 and not any(keyword in list(map(str.lower, explanation.anchor)) for keyword in ['the', 'a', 'an', 'is', 'are', 'was', 'were', 'am', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'shall', 'would', 'should', 'can', 'could', 'may', 'might', 'must', 'ought','need', 'used', 'to', 'of', 'in', 'on','with']):
                    modelConfidence = 'High'
                elif len(explanation.anchor) == 1 and not any(keyword in list(map(str.lower, explanation.anchor)) for keyword in ['the', 'a', 'an', 'is', 'are', 'was', 'were', 'am', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'shall', 'would', 'should', 'can', 'could', 'may', 'might', 'must', 'ought','need', 'used', 'to', 'of', 'in', 'on','with']):
                    modelConfidence = 'Moderate'                    
                elif len(explanation.anchor) == 1 and any(keyword in list(map(str.lower, explanation.anchor)) for keyword in ['the', 'a', 'an', 'is', 'are', 'was', 'were', 'am', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'shall', 'would', 'should', 'can', 'could', 'may', 'might', 'must', 'ought','need', 'used', 'to', 'of', 'in', 'on','with']) or (len(explanation.anchor) == 0):
                    modelConfidence = 'Low'
                result.append({"inputText": inputText, "modelPrediction":prediction, "modelConfidence": modelConfidence, "explanation":explanation.anchor})
            
            dataset = inputData if inputData is not None else dataset[:500]
            # Apply the function to each row in the DataFrame
            dataset[dataset.columns[0]].apply(process_row)
            
            return [{"anchor": result, "description": ANCHOR_TABULAR_DES}]

        except Exception as e:
            # Log the error and re-raise the exception
            log.error(e, exc_info=True)
            raise

    def integrated_gradients_text_local_explanation(params: dict):
        log.info("Running Local Explanation for Unstructured Text Data using Integrated Gradients")
        try:

            model = params['model']
            dataset = params['dataset']
            preprocessor = params['preprocessor']
            targetClassNames = params['targetClassNames']
            
            result=[]
            def process_row(row):
                
                inputText = row
                if preprocessor is not None:
                    tokenized_sentence = preprocessor.texts_to_sequences([inputText])
                    preprocessed_sentence = pad_sequences(tokenized_sentence, padding='post', maxlen=100)
                else:
                    preprocessed_sentence = inputText
                predictions = ((model(preprocessed_sentence).numpy() > 0.5).astype('int32'))[0] # model(preprocessed_sentence).numpy().argmax(axis=1)
               
                layer = model.get_layer('embedding')
                explainer  = IntegratedGradients(model, 
                                                layer=layer, 
                                                n_steps=50, 
                                                method="gausslegendre", 
                                                internal_batch_size=100)
                explanation = explainer.explain(preprocessed_sentence, 
                                                baselines=None, 
                                                target=predictions, 
                                                attribute_to_layer_inputs=False)
                
                # Get attributions values from the explanation object
                attrs = explanation.attributions[0]
                attrs = attrs.sum(axis=2)
                prediction = targetClassNames[predictions[0]]

                words = inputText.split(" ")
                colors = ResponsibleAIExplain.colorize(attrs[0])
                result.append({"inputText":inputText,"modelConfidence": 'Moderate', "prediction": prediction, "explanation": "".join(list(map(ResponsibleAIExplain.hlstr, words, colors)))})
            # if dataset is not None:
            dataset[dataset.columns[0]].apply(process_row) 

            return [{"attributionsText": result, "description": INTEGRATED_GRADIENT_DES}]

        except Exception as e:
            log.error(e, exc_info=True)
            raise
        
    def get_explanation(model=None, taskType=None, modelType=None, dataset=None, 
                    preprocessor=None, targetClassLabel=None, 
                    targetClassNames=None, method=None, scope=None, lineDataset=None, inputIndex=None,
                    api_input_request=None, api_output_response=None):
        try:
            # Prepare the parameters
            params = {
                        "model": model,
                        "taskType": taskType,
                        "modelType": modelType,  
                        "dataset": dataset,
                        "preprocessor": preprocessor,
                        "targetClassLabel": targetClassLabel,
                        "targetClassNames": targetClassNames,
                        "method": method,
                        "scope": scope,
                        "lineDataset": lineDataset,
                        "inputIndex": inputIndex,
                        "api_input_request": api_input_request,
                        "api_output_response": api_output_response
                        }
            
            # Define the mapping between methods and their corresponding functions
            dict_local_explain_mapping = {
                "LOCAL" : {
                            "ANCHOR-TABULAR": ResponsibleAIExplain.anchor_tabular_local_explanation,
                            "KERNEL-SHAP": ResponsibleAIExplain.kernel_shap_local_explanation,
                            "TREE-SHAP": ResponsibleAIExplain.tree_shap_local_explanation,
                            "LIME-TABULAR": ResponsibleAIExplain.lime_tabular_local_explanation,
                            "TS-LIME-TABULAR": ResponsibleAIExplain.timeSeries_local_explanation_lime,
                            "TEXT-SHAP-EXPLAINER": ResponsibleAIExplain.text_shap_local_explanation,
                            "ANCHOR-TEXT": ResponsibleAIExplain.anchor_text_local_explanation,
                            "INTEGRATED-GRADIENTS": ResponsibleAIExplain.integrated_gradients_text_local_explanation
                        },
                "GLOBAL": {
                            "KERNEL-SHAP": ResponsibleAIExplain.kernel_shap_global_explanation,
                            "TS-KERNEL-EXPLAINER": ResponsibleAIExplain.timeSeries_global_explanation,
                            "TREE-SHAP": ResponsibleAIExplain.tree_shap_global_explanation,
                            "PERMUTATION-IMPORTANCE": ResponsibleAIExplain.permutation_importance_global_explanation,
                            "PD-VARIANCE": ResponsibleAIExplain.partial_dependence_variance_global_explanation
                        }
            }
            
            # Call the corresponding function based on the method and return the result
            return dict_local_explain_mapping[scope][method](params)

        except Exception as e:
            # Log the error and re-raise the exception
            log.error(e, exc_info=True)
            raise
