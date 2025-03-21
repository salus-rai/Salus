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

import os
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]="0"
import numpy as np
import pandas as pd
from alibi.explainers import AnchorText
from alibi.explainers import AnchorImage
from alibi.explainers import PartialDependenceVariance
from alibi.explainers import TreeShap
from alibi.explainers import KernelShap
from alibi.explainers import AnchorTabular
from alibi.explainers.shap_wrappers import sum_categories
from alibi.utils import gen_category_map
from sklearn import preprocessing
from sklearn.impute import SimpleImputer
from explain.config.logger import CustomLogger
from sklearn.model_selection import train_test_split
from datetime import  datetime
import cv2
import joblib

local_explain_text_demo_model = joblib.load('../models/demo/local_explain_text/localtext_explain_model.pkl')
local_explain_text_demo_vectorizer = joblib.load('../models/demo/local_explain_text/localtext_explain_vectorizer.pkl')
local_explain_text_demo_predict_fn = lambda x: local_explain_text_demo_model.predict(local_explain_text_demo_vectorizer.transform(x))
local_explainer_text_demo = AnchorText.load('../models//alibi//', predictor=local_explain_text_demo_predict_fn)

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

        return X_split, y_split



    def local_explain_image(inputImage,
                            model,
                            segmentation_fn):
        try:

            image_shape = (299, 299, 3)

            predict_fn = lambda x: model.predict(x)

            explainer = AnchorImage(predict_fn, image_shape, segmentation_fn=segmentation_fn,
                                    images_background=None)
            resizedImage = cv2.resize(inputImage, (299, 299))
            explanation = explainer.explain(resizedImage, threshold=.95, p_sample=.5)
            return { "segments":explanation.segments,"anchor":explanation.anchor }


        except Exception as e:
            log.error(e, exc_info=True)
            raise Exception


    def local_explain_tabular(dataset,
                       inputIndex,
                       model,
                       preprocessor,
                       featureNames,
                       categoricalFeatureNames,
                       targetNames,
                       targetClassNames):

        try:

            log.debug(f"preprocessor: {preprocessor}")
            if preprocessor is not None:
                predict_fn = lambda x: model.predict(preprocessor.transform(x))
            else:
                predict_fn = lambda x: model.predict(x)

            category_map = None
            if categoricalFeatureNames is not None:
                category_map = gen_category_map(dataset,categorical_columns=categoricalFeatureNames)
                log.debug(f"category_map: {category_map}")

            if preprocessor is not None:
                label_encoder = preprocessing.LabelEncoder()
                target = label_encoder.fit_transform(dataset[targetNames])
            else:
                target = dataset[targetNames]

            if targetClassNames is None:
                targetClassNames = dataset[targetNames].unique()

            X = dataset.drop(targetNames, axis=1, inplace=False)
            log.debug(f"X: {X}")
            if featureNames is not None:
                X = X[featureNames]
            else:
                featureNames = list(X.columns.values)

            if preprocessor is not None:
                label_encoder = preprocessing.LabelEncoder()
                column_names = list(X.columns.values)
                for col in column_names:
                    X[col] = label_encoder.fit_transform(X[col])

                imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
                imputer = imputer.fit(X)
                data = imputer.transform(X)
            else:
                data = X

            data_perm = np.random.permutation(np.c_[data, target])
            data = data_perm[:, :-1]
            target = data_perm[:, -1]
            log.debug(f"data: {data}")
            log.debug(f"target: {target}")

            X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.20, train_size=0.80,
                                                                random_state=0)
            explainer = AnchorTabular(
                predictor=predict_fn,
                feature_names=featureNames,
                categorical_names=category_map)

            explainer.fit(X_train, disc_perc=[25, 50, 75])

            explaination = explainer.explain(X_train[inputIndex], threshold=0.95)

            predict_input = X_train[inputIndex].reshape(1, -1)

            prediction = targetClassNames[int(explainer.predictor(predict_input)[0])]
            return {"predictedTarget": str(prediction), "anchor": explaination.anchor}

        except Exception as e:
            log.error(e, exc_info=True)
            return {"predictedTarget": "", "anchor": ""}


    def local_explain_text(text: str,model,vectorizer, class_names):

        log.info("Running local_explain")

        try:

            if vectorizer is not None:
                predict_fn = lambda x: model.predict(vectorizer.transform(x))
            else:
                predict_fn = lambda x: model.predict(x)

            prediction = class_names[predict_fn([text])[0]]

            explainer = AnchorText.load('../models//alibi//', predictor=predict_fn)

            explaination = explainer.explain(text,
                                             threshold=0.95,
                                             stop_on_first=True,
                                             min_samples_start=100,
                                             coverage_samples=100,
                                             verbose=True
                                             )

            return {"predictedTarget": prediction, "anchor": explaination.anchor}

        except Exception as e:
            log.error(e,exc_info=True)
            return {"predictedTarget": prediction, "anchor": explaination.anchor}

    def local_explain_demo(text: str,class_names):

        log.info("Running local_explain")

        try:
            prediction = class_names[local_explain_text_demo_predict_fn([text])[0]]
            explaination = local_explainer_text_demo.explain(text,
                                             threshold=0.95,
                                             stop_on_first=True,
                                             min_samples_start=100,
                                             coverage_samples=100,
                                             verbose=True,
                                             tau=0.5
                                             )

            return {"predictedTarget": prediction, "anchor": explaination.anchor}

        except Exception as e:
            log.error(e,exc_info=True)
            return {"predictedTarget": prediction, "anchor": explaination.anchor}

    def partial_dependence_variance(params: dict):

        try:
            dataset = params['dataset']
            targetNames = params['targetNames']
            model = params['model']
            preprocessor = params['preprocessor']
            categoricalFeatureNames = params["categoricalFeatureNames"]
            targetClassNames = params['targetClassNames']

            if targetClassNames is None:
                targetClassNames = list(dataset[targetNames].unique())

            category_map = None
            if categoricalFeatureNames is not None:
                category_map = gen_category_map(data=dataset, categorical_columns=categoricalFeatureNames)

            X = dataset.drop(targetNames, axis=1, inplace=False)

            column_names = list(X.columns.values)
            if params['featureNames'] is None:
                feature_names = column_names
            else:
                feature_names = params['featureNames']
                X = X[feature_names]
                column_names = list(X.columns.values)


            label_encoder = preprocessing.LabelEncoder()
            for col in column_names:
                X[col] = label_encoder.fit_transform(X[col])

            imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
            imputer = imputer.fit(X)
            X = imputer.transform(X)


            pd_variance = PartialDependenceVariance(predictor=model
                                                    ,target_names=targetClassNames
                                                    ,categorical_names=category_map
                                                    ,feature_names=feature_names)
            exp_importance = pd_variance.explain(X=X,
                                                 method='importance'
                                                 )
            log.debug(f"exp_importance: {exp_importance}")
            data = dict(zip(column_names, exp_importance.feature_importance[0]))
            log.debug(f"data: {data}")
            sorted_data = dict(sorted(data.items(), key = lambda x: x[1], reverse = True))
            log.debug(f"sorted_data: {sorted_data}")

            list_data = []
            features_count = 1
            for k, v in sorted_data.items():
                if features_count <= 5:
                    list_data.append({"featureName": k, "importanceScore": v})
                features_count = features_count + 1

            return [{"importantFeatures":list_data}]



        except Exception as e:
            log.error(e,exc_info=True)
            raise Exception

    def kernel_shap(params: dict):
        try:
            categoricalFeatureNames = params["categoricalFeatureNames"]
            classifier = params['model']
            preprocessor = params['preprocessor']
            dataset = params['dataset']
            targetNames = params['targetNames']
            targetClassNames = params['targetClassNames']

            if targetClassNames is None:
                targetClassNames = list(dataset[targetNames].unique())

            category_map = None
            if categoricalFeatureNames is not None:
                category_map = gen_category_map(data=dataset, categorical_columns=categoricalFeatureNames)

            X = dataset.drop(targetNames, axis=1, inplace=False)

            column_names = list(X.columns.values)
            if params['featureNames'] is None:
                feature_names = column_names
            else:
                feature_names = params['featureNames']
                X = X[feature_names]
                column_names = list(X.columns.values)

            if preprocessor is not None:
                label_encoder = preprocessing.LabelEncoder()
                for col in column_names:
                    X[col] = label_encoder.fit_transform(X[col])

                imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
                imputer = imputer.fit(X)
                data = imputer.transform(X)

                label_encoder = preprocessing.LabelEncoder()
                target = label_encoder.fit_transform(dataset[targetNames])
            else:
                data = X
                target = dataset[targetNames]

            data_perm = np.random.permutation(np.c_[data, target])
            data = data_perm[:, :-1]
            target = data_perm[:, -1]


            X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.20, train_size=0.80,
                                                                random_state=0)
            fraction_explained = 0.05
            X_explain, y_explain = ResponsibleAIExplain.split_set(X_test,
                                                                  y_test,
                                                                  fraction_explained,
                                                                  )

            if preprocessor is not None:
                X_train_proc = preprocessor.transform(X_train)
                X_test_proc = preprocessor.transform(X_test)
                X_explain_proc = preprocessor.transform(X_explain)

                ohe = preprocessor.transformers_[1][1].named_steps['onehot']

                feat_enc_dim = [len(cat_enc) - 1 for cat_enc in ohe.categories_]

                numerical_feats_idx = preprocessor.transformers_[0][2]
                categorical_feats_idx = preprocessor.transformers_[1][2]

                num_feats_names = [feature_names[i] for i in numerical_feats_idx]
                cat_feats_names = [feature_names[i] for i in categorical_feats_idx]

            else:
                X_train_proc = X_train
                X_test_proc = X_test
                X_explain_proc = X_explain
                num_feats_names = feature_names
                cat_feats_names = []

            perm_feat_names = num_feats_names + cat_feats_names

            start_example_idx = 0
            stop_example_idx = 100
            background_data = slice(start_example_idx, stop_example_idx)

            pred_fcn = lambda x: classifier.predict_proba(x)

            lr_explainer = KernelShap(pred_fcn, link='logit', feature_names=perm_feat_names)
            lr_explainer.fit(X_train_proc[background_data, :])

            if category_map is not None:
                ordinal_features = [x for x in range(len(feature_names)) if x not in list(category_map.keys())]
                start = len(ordinal_features)
                cat_feat_start = [start]
                for dim in feat_enc_dim[:-1]:
                    cat_feat_start.append(dim + cat_feat_start[-1])
            else:
                cat_feat_start = None
                feat_enc_dim = None

            background_data_test = slice(params['inputIndex'], params['inputIndex']+1)

            explanation = lr_explainer.explain(X_explain_proc[params['inputIndex']:params['inputIndex']+1],
                                               summarise_result=True,
                                               cat_vars_start_idx=cat_feat_start,
                                               cat_vars_enc_dim=feat_enc_dim
                                               )
            log.debug(f"explanation: {explanation}")
            importances = explanation['data']['raw']['importances']

            log.debug(f"targetClass: {targetClassNames}")
            class_idx = 0

            list_kernel_shap = []
            for item in importances.items():
                log.debug(f"item: {item}")
                if item[0] == 'aggregated':
                    break
                data = dict(zip(item[1]['names'], item[1]['ranked_effect']))
                sorted_data = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))

                features_count = 1
                list_importance = []
                for k, v in sorted_data.items():
                    if features_count > 5:
                        break
                    list_importance.append({"featureName": k, "importanceScore": v})
                    features_count = features_count + 1
                list_kernel_shap.append({"className": targetClassNames[class_idx],
                                         "importantFeatures": list_importance})
                class_idx = class_idx + 1

            return list_kernel_shap

        except Exception as e:
            log.error(e, exc_info=True)
            raise Exception


    def tree_shap(params: dict):
        try:
            categoricalFeatureNames = params["categoricalFeatureNames"]
            model = params['model']
            dataset = params['dataset']
            preprocessor = params['preprocessor']
            targetNames = params['targetNames']
            targetClassNames = params['targetClassNames']

            if targetClassNames is None:
                targetClassNames = list(dataset[targetNames].unique())

            category_map = None
            if categoricalFeatureNames is not None:
                category_map = gen_category_map(data=dataset, categorical_columns=categoricalFeatureNames)

            X = dataset.drop(targetNames, axis=1, inplace=False)

            column_names = list(X.columns.values)
            if params['featureNames'] is None:
                feature_names = column_names
            else:
                feature_names = params['featureNames']
                X = X[feature_names]
                column_names = list(X.columns.values)

            tree_shap_explainer = TreeShap(
                model,
                feature_names=feature_names,
                categorical_names=category_map
            )
            tree_shap_explainer.fit()

            label_encoder = preprocessing.LabelEncoder()
            for col in column_names:
                X[col] = label_encoder.fit_transform(X[col])

            imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
            imputer = imputer.fit(X)
            X = imputer.transform(X)

            explanation = tree_shap_explainer.explain(X)
            log.debug(f"explanation: {explanation}")
            importances = explanation['data']['raw']['importances']

            log.debug(f"targetClass: {targetClassNames}")
            class_idx = 0

            list_tree_shap = []
            for item in importances.items():

                if item[0] == 'aggregated':
                    break
                data = dict(zip(item[1]['names'], item[1]['ranked_effect']))
                sorted_data = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))

                features_count = 1
                list_importance = []
                for k, v in sorted_data.items():
                    if features_count > 5:
                        break
                    list_importance.append({"featureName": k, "importanceScore": v})
                    features_count = features_count + 1
                list_tree_shap.append({"importantFeatures": list_importance})
                class_idx = class_idx + 1
            log.debug(f"list_importance: {list_importance}")
            return list_tree_shap

        except Exception as e:
            log.error(e, exc_info=True)
            raise Exception

    def global_explain(dataset,
                       inputIndex,
                       method,
                       model,
                       preprocessor,
                       featureNames,
                       categoricalFeatureNames,
                       targetNames,
                       targetClassNames):

        try:

            params = {
                "dataset":dataset,
                "inputIndex": inputIndex,
                "model":model,
                "preprocessor":preprocessor,
                "featureNames": featureNames,
                "categoricalFeatureNames":categoricalFeatureNames,
                "targetNames":targetNames,
                "targetClassNames":targetClassNames}

            log.debug(f"method: {method}")

            dict_global_explain_mapping = {
                "PD-VARIANCE": ResponsibleAIExplain.partial_dependence_variance,
                "KERNEL-SHAP": ResponsibleAIExplain.kernel_shap,
                "TREE-SHAP": ResponsibleAIExplain.tree_shap
            }

            return dict_global_explain_mapping[method](params)


        except Exception as e:
            log.error(e,exc_info=True)
            return [{"importantFeatures":[{"featureName": "", "importanceScore": ""}]}]
