from setuptools import setup, find_packages

setup(
    name='trustllm',
    version='0.3.3',
    description='TrustLLM', 
    author='Yue Huang & Siyuan Wu & Haoran Wang',
    author_email='trustllm.benchmark@gmail.com',  
    packages=find_packages(), 
    include_package_data=True, 
    install_requires=[
        'transformers',
        'huggingface_hub',
        'peft',
        'numpy>=1.18.1',
        'scipy==1.11.4',
        'pandas>=1.0.3',
        'scikit-learn',
        'openai==0.28.0',
        'tqdm',
        'tenacity',
        'datasets',
        'fschat[model_worker]',
        'python-dotenv',
        'urllib3',
        'anthropic',
        'google.generativeai',
        'google-api-python-client',
        'google.ai.generativelanguage',
        'replicate',
        'zhipuai>=2.0.1'
],
    classifiers=[
    ],
)
