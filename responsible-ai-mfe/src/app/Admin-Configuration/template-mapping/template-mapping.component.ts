/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { Component, Input, ViewChild } from '@angular/core';
import { MatSelect, MatSelectChange } from '@angular/material/select';
import { MatOption } from '@angular/material/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { UserValidationService } from 'src/app/services/user-validation.service';

@Component({
  selector: 'app-template-mapping',
  templateUrl: './template-mapping.component.html',
  styleUrls: ['./template-mapping.component.css']
})
export class TemplateMappingComponent {
  



  @ViewChild('select2') select2!: MatSelect;
  @ViewChild('select3') select3!: MatSelect;
  @ViewChild('select4') select4!: MatSelect;
  @ViewChild('select5') select5!: MatSelect;
  @Input() parPortfolio!: any;
  @Input() parAccount!: any;
  result: any;
  dataSource_getBatches: any;
  templateMappingGetUrl: any;
  Admin_getModMaps: any;

  constructor (private fb: FormBuilder,public _snackBar: MatSnackBar, private https: HttpClient, public dialog: MatDialog,public validationService : UserValidationService){
    this.form = this.fb.group({
      options: [null, Validators.required]
    });
  }


// SCREEN TWO ADD DATA  
//--------------VARIABLES-----------SECURITY

category: any = [];
subcategory: any = [];
selectedReclist: any = [];
selectedReclist2: any = [];
allSelectedInput = false;
event1: any;
c1: boolean = false;
allSelected2: any;
listShowlist2 = new Set();
allSelectedInput2 = false;
event2: any;
c2: boolean = false;
userId =""
tab="Privacy"
dataSource: any = []
listReconList: any=[];
  customTemplateGetUrl: string="";
  responseArr:any=[]
  requestArr:any=[]
  tempalteArray:any=[]
  tempalteArray2:any=[]
  templateMappingPostUrl=""
  selectedReclist3: any = [];
  allSelected3: any;
listShowlist3 = new Set();
allSelectedInput3 = false;
event3: any;
c3: boolean = false;
  selectedReclist4: any = [];
  allSelected4: any;
listShowlist4 = new Set();
allSelectedInput4 = false;
event4: any;
c4: boolean = false;
  selectedReclist5: any = [];
  allSelected5: any;
listShowlist5 = new Set();
allSelectedInput5 = false;
event5: any;
c5: boolean = false;
masterTemplateArr :any = ["Prompt Injection Check","Jailbreak Check","TOXICITY","PIIDETCT","REFUSAL","PROFANITY","RESTRICTTOPIC","Fairness and Bias Check"]
categoryList :any = [{viewValue:"Single Model",value:"SingleModel",},{viewValue:"Multi Model",value:"MultiModel"},]
disabledsubcategoryList :any = []
subcategoryList :any = ["Model","Template",]
options :any = ["Model","Template",]
options3 :any =["TextTemplate","TextModel","ImageTemplate","ImageModel"]
RequestTextDropDownArr:any=["PromptInjection", "JailBreak", "Toxicity", "Piidetct", "Refusal", "Profanity", "RestrictTopic", "TextQuality", "CustomizedTheme"]
ResponseTextDropDownArr:any=["Toxicity", "Piidetct", "Refusal", "Profanity", "RestrictTopic", "TextQuality", "TextRelevance"]
RequestImageTemplateDropDownArr:any=["PromptInjection", "JailBreak", "Toxicity","Profanity", "RestrictTopic"]

// for new ui

RequestSingleModelDropDownArr:any=["PromptInjection", "JailBreak", "Toxicity", "Piidetct", "Refusal", "Profanity", "RestrictTopic", "TextQuality", "CustomizedTheme"]
ResponseSingleModelDropDownArr:any=["Toxicity", "Piidetct", "Refusal", "Profanity", "RestrictTopic", "TextQuality", "TextRelevance"]

RequestSingleTemplateDropDownArr:any=[]
ResponseSingleTemplateDropDownArr:any=[]
RequestMultipleTemplateDropDownArr:any=[]
ResponseMultipleTemplateDropDownArr:any=[]
RequestMultipleImageModelDropDownArr:any= [ "Privacy","Profanity"]

// RequestMultipleTextTemplateDropDownArr:any=["PromptInjection", "JailBreak", "Toxicity", "Piidetct", "Refusal", "Profanity", "RestrictTopic", "TextQuality", "CustomizedTheme"]
// ResponseMultipleTextTemplateDropDownArr:any=["Toxicity", "Piidetct", "Refusal", "Profanity", "RestrictTopic", "TextQuality", "TextRelevance"]

comparsionDropDownArr:any=[]
requestDropDownArr:any=[]
resonseDropDownArr:any=[]

roles: any;
panelOpenState = false;
// selectedOptions: any = []
selectedOptions: { [key: string]: boolean } = {};
selectedOptions3: { [key: string]: boolean } = {};

dropdownloader:boolean = false
bodydisabledSatatus:boolean = true

tenantarr: any = []

form: FormGroup;

viewoptions() {
  // console.log("Array===",this.selectedOptions)
  // [Privacy: true, Profanity: true, Explainability: true, FM-Moderation: true]
  const myObject = { ...this.selectedOptions };
  console.log("myObject===", myObject)
  const filteredKeys = this.filterKeysByBoolean(myObject);
  console.log("only keys", filteredKeys);
  this.tenantarr = filteredKeys

  this.form.patchValue({
    options: this.tenantarr
  });

}

filterKeysByBoolean(obj: Record<string, boolean>): string[] {
  return Object.keys(obj).filter((key) => obj[key]);
}

  // select 1
  @ViewChild('select1') select1!: MatSelect;
  allSelected1: any;
listShowlist1 = new Set();
toggleAllSelection1(event: any) {
  this.event1 = event;
  this.c1 = event.checked;
  this.allSelected1 = !this.allSelected1;
  if (this.allSelected1) {
    this.select1.options.forEach((item: MatOption) => {
      item.select();
      this.listShowlist1.add(item.value);
      const element = document.querySelector('[role="listbox"]');
      if (element instanceof HTMLElement) {
        element.style.display = 'none';
      }
      this.select1.close();
    });
  } else {
    this.select1.options.forEach((item: MatOption) => {
      item.deselect();

      this.listShowlist1.delete(item.value);
    });
  }
}
selectRecognizertype() {
  let newStatus = true;
  this.select1.options.forEach((item: MatOption) => {
    if (!item.selected) {
      newStatus = false;
      this.allSelected1 = false;
      this.listShowlist1.delete(item.value);
    } else {
      this.listShowlist1.add(item.value);
    }
  });
  this.allSelectedInput = newStatus;
}

  // select 2
  toggleAllSelection2(event: any) {
    this.event2 = event;
    this.c2 = event.checked;
    this.allSelected2 = !this.allSelected2;
    if (this.allSelected2) {
      this.select2.options.forEach((item: MatOption) => {
        item.select();
        this.listShowlist2.add(item.value);
        const element = document.querySelector('[role="listbox"]');
        if (element instanceof HTMLElement) {
          element.style.display = 'none';
        }
        this.select2.close();
      });
    } else {
      this.select2.options.forEach((item: MatOption) => {
        item.deselect();
  
        this.listShowlist2.delete(item.value);
      });
    }
  }
  selectRecognizertype2() {
    let newStatus = true;
    this.select2.options.forEach((item: MatOption) => {
      if (!item.selected) {
        newStatus = false;
        this.allSelected2 = false;
        this.listShowlist2.delete(item.value);
      } else {
        this.listShowlist2.add(item.value);
      }
    });
    this.allSelectedInput2 = newStatus;
  }


    // select 1
toggleAllSelection3(event: any) {
  this.event3 = event;
  this.c3 = event.checked;
  this.allSelected3 = !this.allSelected3;
  if (this.allSelected3) {
    this.select3.options.forEach((item: MatOption) => {
      item.select();
      this.listShowlist3.add(item.value);
      const element = document.querySelector('[role="listbox"]');
      if (element instanceof HTMLElement) {
        element.style.display = 'none';
      }
      this.select3.close();
    });
  } else {
    this.select3.options.forEach((item: MatOption) => {
      item.deselect();

      this.listShowlist3.delete(item.value);
    });
  }
}
selectRecognizertype3() {
  let newStatus = true;
  this.select3.options.forEach((item: MatOption) => {
    if (!item.selected) {
      newStatus = false;
      this.allSelected3 = false;
      this.listShowlist3.delete(item.value);
    } else {
      this.listShowlist3.add(item.value);
    }
  });
  this.allSelectedInput3 = newStatus;
}
// select 4 category
toggleAllSelection4(event: any) {
  this.event4 = event;
  this.c4 = event.checked;
  this.allSelected4 = !this.allSelected4;
  if (this.allSelected4) {
    this.select4.options.forEach((item: MatOption) => {
      item.select();
      this.listShowlist4.add(item.value);
      const element = document.querySelector('[role="listbox"]');
      if (element instanceof HTMLElement) {
        element.style.display = 'none';
      }
      this.select4.close();
    });
  } else {
    this.select4.options.forEach((item: MatOption) => {
      item.deselect();

      this.listShowlist4.delete(item.value);
    });
  }
}
selectRecognizertype4() {
  let newStatus = true;
  this.select4.options.forEach((item: MatOption) => {
    if (!item.selected) {
      newStatus = false;
      this.allSelected4 = false;
      this.listShowlist4.delete(item.value);
    } else {
      this.listShowlist4.add(item.value);
    }
  });
  this.allSelectedInput4 = newStatus;
}
// select 5 sub-category
toggleAllSelection5(event: any) {
  this.event5 = event;
  this.c5 = event.checked;
  this.allSelected5 = !this.allSelected5;
  if (this.allSelected5) {
    this.select4.options.forEach((item: MatOption) => {
      item.select();
      this.listShowlist5.add(item.value);
      const element = document.querySelector('[role="listbox"]');
      if (element instanceof HTMLElement) {
        element.style.display = 'none';
      }
      this.select5.close();
    });
  } else {
    this.select5.options.forEach((item: MatOption) => {
      item.deselect();

      this.listShowlist5.delete(item.value);
    });
  }
}
selectRecognizertype5() {
  let newStatus = true;
  this.select5.options.forEach((item: MatOption) => {
    if (!item.selected) {
      newStatus = false;
      this.allSelected5 = false;
      this.listShowlist5.delete(item.value);
    } else {
      this.listShowlist5.add(item.value);
    }
  });
  this.allSelectedInput5 = newStatus;
}

// for new ui 
selectedModelRequest: any[] = [];
  selectedModelResponse: any[] = [];
  selectedTemplateRequest: any[] = [];
  selectedTemplateResponse: any[] = [];
  selectedTextTemplateRequest: any[] = [];
  selectedTextTemplateResponse: any[] = [];
  selectedTextModelRequest: any[] = [];
  selectedTextModelResponse: any[] = [];
  selectedImageTemplateRequest: any[] = [];
  selectedImageModelRequest: any[] = [];
//
@ViewChild('selectModelRequest1') selectModelRequest1!: MatSelect;
@ViewChild('selectModelResponse1') selectModelResponse1!: MatSelect;
@ViewChild('selectTemplateRequest1') selectTemplateRequest1!: MatSelect;
@ViewChild('selectTemplateResponse1') selectTemplateResponse1!: MatSelect;
@ViewChild('selectTextTemplateRequest1') selectTextTemplateRequest1!: MatSelect;
@ViewChild('selectTextTemplateResponse1') selectTextTemplateResponse1!: MatSelect;
@ViewChild('selectTextModelRequest1') selectTextModelRequest1!: MatSelect;
@ViewChild('selectTextModelResponse1') selectTextModelResponse1!: MatSelect;
@ViewChild('selectImageTemplateRequest1') selectImageTemplateRequest1!: MatSelect;
@ViewChild('selectImageModelRequest1') selectImageModelRequest1!: MatSelect;

allSelectedModelRequest1: any;
allSelectedModelResponse1: any;
allSelectedTemplateRequest1: any;
allSelectedTemplateResponse1: any;
allSelectedTextTemplateRequest1: any;
allSelectedTextTemplateResponse1: any;
allSelectedTextModelRequest1: any;
allSelectedTextModelResponse1: any;
allSelectedImageTemplateRequest1: any;
allSelectedImageModelRequest1: any;

listShowlistModelRequest1 = new Set();
listShowlistModelResponse1 = new Set();
listShowlistTemplateRequest1 = new Set();
listShowlistTemplateResponse1 = new Set();
listShowlistTextTemplateRequest1 = new Set();
listShowlistTextTemplateResponse1 = new Set();
listShowlistTextModelRequest1 = new Set();
listShowlistTextModelResponse1 = new Set();
listShowlistImageTemplateRequest1 = new Set();
listShowlistImageModelRequest1 = new Set();

toggleAllSelectionModelRequest1(event: any) {
  this.toggleAllSelection(event, this.selectModelRequest1, this.listShowlistModelRequest1, 'allSelectedModelRequest1');
}

toggleAllSelectionModelResponse1(event: any) {
  this.toggleAllSelection(event, this.selectModelResponse1, this.listShowlistModelResponse1, 'allSelectedModelResponse1');
}

toggleAllSelectionTemplateRequest1(event: any) {
  this.toggleAllSelection(event, this.selectTemplateRequest1, this.listShowlistTemplateRequest1, 'allSelectedTemplateRequest1');
}

toggleAllSelectionTemplateResponse1(event: any) {
  this.toggleAllSelection(event, this.selectTemplateResponse1, this.listShowlistTemplateResponse1, 'allSelectedTemplateResponse1');
}

toggleAllSelectionTextTemplateRequest1(event: any) {
  this.toggleAllSelection(event, this.selectTextTemplateRequest1, this.listShowlistTextTemplateRequest1, 'allSelectedTextTemplateRequest1');
}

toggleAllSelectionTextTemplateResponse1(event: any) {
  this.toggleAllSelection(event, this.selectTextTemplateResponse1, this.listShowlistTextTemplateResponse1, 'allSelectedTextTemplateResponse1');
}

toggleAllSelectionTextModelRequest1(event: any) {
  this.toggleAllSelection(event, this.selectTextModelRequest1, this.listShowlistTextModelRequest1, 'allSelectedTextModelRequest1');
}

toggleAllSelectionTextModelResponse1(event: any) {
  this.toggleAllSelection(event, this.selectTextModelResponse1, this.listShowlistTextModelResponse1, 'allSelectedTextModelResponse1');
}

toggleAllSelectionImageTemplateRequest1(event: any) {
  this.toggleAllSelection(event, this.selectImageTemplateRequest1, this.listShowlistImageTemplateRequest1, 'allSelectedImageTemplateRequest1');
}

toggleAllSelectionImageModelRequest1(event: any) {
  this.toggleAllSelection(event, this.selectImageModelRequest1, this.listShowlistImageModelRequest1, 'allSelectedImageModelRequest1');
}

toggleAllSelection(event: any, select: MatSelect, listShowlist: Set<any>, allSelectedKey: keyof TemplateMappingComponent & string) {
  (this as any)[allSelectedKey] = !(this as any)[allSelectedKey];
  if ((this as any)[allSelectedKey]) {
    select.options?.forEach((item: MatOption) => {
      item.select();
      listShowlist.add(item.value);
      const element = document.querySelector('[role="listbox"]');
      if (element instanceof HTMLElement) {
        element.style.display = 'none';
      }
      select.close();
    });
  } else {
    select.options?.forEach((item: MatOption) => {
      item.deselect();
      listShowlist.delete(item.value);
    });
  }
}

updateSelectionStatusModelRequest1() {
  this.updateSelectionStatus(this.selectModelRequest1, this.listShowlistModelRequest1, 'allSelectedModelRequest1');
}

updateSelectionStatusModelResponse1() {
  this.updateSelectionStatus(this.selectModelResponse1, this.listShowlistModelResponse1, 'allSelectedModelResponse1');
}

updateSelectionStatusTemplateRequest1() {
  this.updateSelectionStatus(this.selectTemplateRequest1, this.listShowlistTemplateRequest1, 'allSelectedTemplateRequest1');
}

updateSelectionStatusTemplateResponse1() {
  this.updateSelectionStatus(this.selectTemplateResponse1, this.listShowlistTemplateResponse1, 'allSelectedTemplateResponse1');
}

updateSelectionStatusTextTemplateRequest1() {
  this.updateSelectionStatus(this.selectTextTemplateRequest1, this.listShowlistTextTemplateRequest1, 'allSelectedTextTemplateRequest1');
}

updateSelectionStatusTextTemplateResponse1() {
  this.updateSelectionStatus(this.selectTextTemplateResponse1, this.listShowlistTextTemplateResponse1, 'allSelectedTextTemplateResponse1');
}

updateSelectionStatusTextModelRequest1() {
  this.updateSelectionStatus(this.selectTextModelRequest1, this.listShowlistTextModelRequest1, 'allSelectedTextModelRequest1');
}

updateSelectionStatusTextModelResponse1() {
  this.updateSelectionStatus(this.selectTextModelResponse1, this.listShowlistTextModelResponse1, 'allSelectedTextModelResponse1');
}

updateSelectionStatusImageTemplateRequest1() {
  this.updateSelectionStatus(this.selectImageTemplateRequest1, this.listShowlistImageTemplateRequest1, 'allSelectedImageTemplateRequest1');
}

updateSelectionStatusImageModelRequest1() {
  this.updateSelectionStatus(this.selectImageModelRequest1, this.listShowlistImageModelRequest1, 'allSelectedImageModelRequest1');
}

updateSelectionStatus(select: MatSelect, listShowlist: Set<any>, allSelectedKey: keyof TemplateMappingComponent & string) {
  let newStatus = true;
  select.options?.forEach((item: MatOption) => {
    if (!item.selected) {
      newStatus = false;
      (this as any)[allSelectedKey] = false;
      listShowlist.delete(item.value);
    } else {
      listShowlist.add(item.value);
    }
  });
  (this as any)[allSelectedKey] = newStatus;
}
  

// 
// submit for new ui
submitSingleModel() {
  const selectedModelRequest = this.selectedModelRequest;
  const selectedModelResponse = this.selectedModelResponse;
  const selectedTemplateRequest = this.selectedTemplateRequest;
  const selectedTemplateResponse = this.selectedTemplateResponse;

  // Process or log the selected values
  console.log('Selected Model Request:', selectedModelRequest);
  console.log('Selected Model Response:', selectedModelResponse);
  console.log('Selected Template Request:', selectedTemplateRequest);
  console.log('Selected Template Response:', selectedTemplateResponse);

  // Add further processing logic as needed
}
submitMultiModel() {
  const selectedTextTemplateRequest = this.selectedTextTemplateRequest;
  const selectedTextTemplateResponse = this.selectedTextTemplateResponse;
  const selectedTextModelRequest = this.selectedTextModelRequest;
  const selectedTextModelResponse = this.selectedTextModelResponse;
  const selectedImageTemplateRequest = this.selectedImageTemplateRequest;
  const selectedImageModelRequest = this.selectedImageModelRequest;

  // Process or log the selected values
  console.log('Selected Text Template Request:', selectedTextTemplateRequest);
  console.log('Selected Text Template Response:', selectedTextTemplateResponse);
  console.log('Selected Text Model Request:', selectedTextModelRequest);
  console.log('Selected Text Model Response:', selectedTextModelResponse);
  console.log('Selected Image Template Request:', selectedImageTemplateRequest);
  console.log('Selected Image Model Request:', selectedImageModelRequest);

  // Add further processing logic as needed
}
// 
categoryslected: boolean = false
categoryChange(event: MatSelectChange){
  this.categoryslected= true
  if(event.value == "SingleModel"){
    this.subcategoryList=["Model","Template"]
  }else if(event.value == "MultiModel"){
    this.subcategoryList=["TextTemplate","TextModel","ImageTemplate","ImageModel"
      //,"ImageModel" this not yet functional for now will be added later 
    ]
  }
  this.getAccountModule()

}
showresponseDropdownforTemp= true
subcategoryChange(event: MatSelectChange)
{
  if ((event.value == "Model" && this.category == "SingleModel") || (event.value == "TextModel" && this.category == "MultiModel")) {
    this.requestDropDownArr = ["PromptInjection", "JailBreak", "Toxicity", "Piidetct", "Refusal", "Profanity", "RestrictTopic", "TextQuality", "CustomizedTheme"]
    this.resonseDropDownArr = ["Toxicity", "Piidetct", "Refusal", "Profanity", "RestrictTopic", "TextQuality", "TextRelevance"]
    this.showresponseDropdownforTemp= true
  }
  else if (event.value == "ImageModel" && this.category == "MultiModel") {
    // this.requestDropDownArr = ["PromptInjection", "JailBreak", "Toxicity","Profanity", "RestrictTopic"]
    this.requestDropDownArr = [ "Privacy","Profanity"]
    this.showresponseDropdownforTemp= false
  }
  else if (event.value == "ImageTemplate" && this.category == "MultiModel") {
    // this.requestDropDownArr = ["PromptInjection", "JailBreak", "Toxicity","Profanity", "RestrictTopic"]
    this.getTemplateDetail()
    this.showresponseDropdownforTemp= false
  }
  else if (event.value == "TextTemplate" && this.category == "MultiModel") {
    // this.requestDropDownArr = ["PromptInjection", "JailBreak", "Toxicity","Profanity", "RestrictTopic"]
    this.getTemplateDetailSingle()
    this.showresponseDropdownforTemp= false
  }
  else {
    this.showresponseDropdownforTemp= true
    this.getTemplateDetail()
  }
    
  
  
 

}


  submit(){

    const payload = {
      "userId": this.userId,
      "portfolio": this.parPortfolio,
      "account": this.parAccount,
      "category": this.category,
      "subcategory": this.subcategory,
      "requestTemplate": this.selectedReclist,
      "responseTemplate": this.selectedReclist2,
      "comparisonTemplate": this.selectedReclist3
    }


    console.log("payload===",payload)
    console.log("=============",this.templateMappingPostUrl)
    this.https.post(this.templateMappingPostUrl,payload).subscribe((res)=>{
      console.log("res=================",res)
      // this.CustomTemplateForm.reset()
      // this.tempalteArray=[]
      this.selectedReclist=[]
      this.selectedReclist2=[]
      this.selectedReclist3=[]
      // this.getTemplateDetail()
      
      this._snackBar.open("Template Saved Successfully", "Close", {
        duration: 2000,
      });
    }, error => {
      // You can access status:
      console.log(error.status);


      // console.log(error.error.detail)
      console.log(error)
      const message = (error.error && (error.error.detail || error.error.message)) || "The Api has failed"
      const action = "Close"
      this._snackBar.open(message, action, {
        duration: 3000,
        horizontalPosition: 'left',
        panelClass: ['le-u-bg-black'],
      });


    })

  }
 

  getTemplateDetail(){
    console.log("inside getTemplateDetail")
    let temptempalteArray:any= []
    // const url = 'http://localhost:30016/api/v1/rai/admin/getCustomeTemplate/';
    const url = this.customTemplateGetUrl;
    const params = new HttpParams()

      .set('category',this.category);
    // let urlx = `${url}${this.userId}`
    let urlx = `${this.customTemplateGetUrl}${this.userId}`

    this.https.get(urlx, { params, headers: { 'accept': 'application/json' } })
      .subscribe
    // this.https.get(this.customTemplateGetUrl+this.userId+this.category).subscribe
    ((res: any) => {
     
      this.result = res
      console.log("this.result===",this.result)
      this.dataSource_getBatches = res.templates;
      for(let i=0;i<this.dataSource_getBatches.length;i++){
        temptempalteArray.push(this.dataSource_getBatches[i].templateName)
        // this.tempalteArray2.push(this.dataSource_getBatches[i].templateName)
        
        // this.tempalteArray.push(this.)
      }
      this.requestDropDownArr = temptempalteArray
      this.RequestSingleTemplateDropDownArr = temptempalteArray
      this.ResponseSingleTemplateDropDownArr= temptempalteArray
      this.resonseDropDownArr = temptempalteArray
      // this.comparsionDropDownArr = this.tempalteArray // made changes on 8/28/2024
      this.comparsionDropDownArr = []
      console.log("this.masterTemplateArr===",this.masterTemplateArr)
      // this.tempalteArray = this.masterTemplateArr.concat(this.tempalteArray);  // made changes on 8/28/2024
      console.log("this.tempalteArray===", this.tempalteArray);

    }  , error => {
 
 
      // this.showSpinner1 = false;

      // console.log(error.error.detail)
      console.log(error)
      const message = (error.error && (error.error.detail || error.error.message)) || "The Api has failed"
      const action = "Close"
      this._snackBar.open(message, action, {
        duration: 3000,
        panelClass:['le-u-bg-black'],
      });

  })
    
}
  getTemplateDetailMultiple(){
    console.log("inside getTemplateDetailMultiple")
    let temptempalteArray:any= []
    // const url = 'http://localhost:30016/api/v1/rai/admin/getCustomeTemplate/';
    const url = this.customTemplateGetUrl;
    const params = new HttpParams()

      .set('category',"MultiModel");
    // let urlx = `${url}${this.userId}`
    let urlx = `${this.customTemplateGetUrl}${this.userId}`

    this.https.get(urlx, { params, headers: { 'accept': 'application/json' } })
      .subscribe
    // this.https.get(this.customTemplateGetUrl+this.userId+this.category).subscribe
    ((res: any) => {
     
      this.result = res
      console.log("this.result===",this.result)
      this.dataSource_getBatches = res.templates;
      for(let i=0;i<this.dataSource_getBatches.length;i++){
        temptempalteArray.push(this.dataSource_getBatches[i].templateName)
        // this.tempalteArray2.push(this.dataSource_getBatches[i].templateName)
        
        // this.tempalteArray.push(this.)
      }
      // this.requestDropDownArr = temptempalteArray
      this.RequestMultipleTemplateDropDownArr = temptempalteArray // for image template
      this.ResponseMultipleTemplateDropDownArr= temptempalteArray // for image template
      // this.resonseDropDownArr = temptempalteArray
      // this.comparsionDropDownArr = this.tempalteArray // made changes on 8/28/2024
      // this.comparsionDropDownArr = []
      console.log("this.masterTemplateArr===",this.masterTemplateArr)
      // this.tempalteArray = this.masterTemplateArr.concat(this.tempalteArray);  // made changes on 8/28/2024
      // console.log("this.tempalteArray===", this.tempalteArray);

    }  , error => {
 
 
      // this.showSpinner1 = false;

      // console.log(error.error.detail)
      console.log(error)
      const message = (error.error && (error.error.detail || error.error.message)) || "The Api has failed"
      const action = "Close"
      this._snackBar.open(message, action, {
        duration: 3000,
        panelClass:['le-u-bg-black'],
      });

  })
    
}
  getTemplateDetailSingle(){
    console.log("inside getTemplateDetail single")
    let temptempalteArray:any= []
    // const url = 'http://localhost:30016/api/v1/rai/admin/getCustomeTemplate/';
    const url = this.customTemplateGetUrl;
    const params = new HttpParams()

      .set('category',"SingleModel");
    // let urlx = `${url}${this.userId}`
    let urlx = `${this.customTemplateGetUrl}${this.userId}`

    this.https.get(urlx, { params, headers: { 'accept': 'application/json' } })
      .subscribe
    // this.https.get(this.customTemplateGetUrl+this.userId+this.category).subscribe
    ((res: any) => {
     
      this.result = res
      console.log("this.result===",this.result)
      this.dataSource_getBatches = res.templates;
      for(let i=0;i<this.dataSource_getBatches.length;i++){
        temptempalteArray.push(this.dataSource_getBatches[i].templateName)
        // this.tempalteArray2.push(this.dataSource_getBatches[i].templateName)
        
        // this.tempalteArray.push(this.)
      }
      // this.requestDropDownArr = temptempalteArray
      this.RequestSingleTemplateDropDownArr = temptempalteArray
      this.ResponseSingleTemplateDropDownArr= temptempalteArray
      
      // this.resonseDropDownArr = temptempalteArray
      // this.comparsionDropDownArr = this.tempalteArray // made changes on 8/28/2024
      // this.comparsionDropDownArr = []
      // console.log("this.masterTemplateArr===",this.masterTemplateArr)
      // this.tempalteArray = this.masterTemplateArr.concat(this.tempalteArray);  // made changes on 8/28/2024
      // console.log("this.tempalteArray===", this.tempalteArray);

    }  , error => {
 
 
      // this.showSpinner1 = false;

      // console.log(error.error.detail)
      console.log(error)
      const message = (error.error && (error.error.detail || error.error.message)) || "The Api has failed"
      const action = "Close"
      this._snackBar.open(message, action, {
        duration: 3000,
        panelClass:['le-u-bg-black'],
      });

  })
    
}


  getLogedInUser() {
    let role = localStorage.getItem('role');
    console.log("role267===",role)
    if (window && window.localStorage && typeof localStorage !== 'undefined') {
      const x = localStorage.getItem("userid") ? JSON.parse(localStorage.getItem("userid")!) : "NA";
      if (x != null && (this.validationService.isValidEmail(x) || this.validationService.isValidName(x))) {
        this.userId = x ;
      }
      console.log("userId", this.userId)
    }

  }
  sanitizeInput(input: any) {
     // Allow alphanumeric characters, @, and .
     return input.replace(/[^a-zA-Z0-9@.]/g, '');
}
  getLocalStoreApi() {
    let ip_port
    if (localStorage.getItem("res") != null) {
      const x = localStorage.getItem("res")
      if (x != null) {
        return ip_port = JSON.parse(x)
      }
    }
  }

  setApilist(ip_port: any) {
      this.templateMappingPostUrl=ip_port.result.Admin + ip_port.result.ACCTEMPMAP 
    this.customTemplateGetUrl=ip_port.result.Admin + ip_port.result.TemplateGet
    this.templateMappingGetUrl=ip_port.result.Admin + ip_port.result.GETACCTEMPMAP  
    this.Admin_getModMaps=ip_port.result.Admin + ip_port.result.Admin_getModMaps  
    

    
  }

  getAccountModule() {
    // const url = 'http://localhost:30016/api/v1/rai/admin/getModMaps';
    // const url = 'https://rai-toolkit-dev.az.ad.idemo-ppc.com/api/v1/rai/admin/getModMaps';
    const url = this.Admin_getModMaps;
    const params = new HttpParams()
      .set('userid', this.userId,)
      .set('portfolio',this.parPortfolio)
      .set('account', this.parAccount);

    this.https.get(url, { params, headers: { 'accept': 'application/json' } })
      .subscribe(
        (response:any) => {
          if (!response || (Array.isArray(response) && response.length === 0)) {
            console.log('Response is empty');
            this.bodydisabledSatatus = false
            this.disabledsubcategoryList=[]
            // Handle empty response here
          } else {
            console.log('Response:', response);
            // Handle the response here
            if (response.SingleModel) {
              if(response.SingleModel.Model){
                this.disabledsubcategoryList.push('Model');
              }
              if (response.SingleModel.Template) {
                this.disabledsubcategoryList.push('Template');
              }
            }
            if (response.MultiModel) {
              if(response.MultiModel.TextTemplate){
                this.disabledsubcategoryList.push('TextTemplate');
              }
              if (response.MultiModel.TextModel) {
                this.disabledsubcategoryList.push('TextModel');
              }
              if (response.MultiModel.ImageTemplate) {
                this.disabledsubcategoryList.push('ImageTemplate');
              }
              if (response.MultiModel.ImageModel) {
                this.disabledsubcategoryList.push('ImageModel');
              }
            }
          }
          console.log("this.disabledsubcategoryList===",this.disabledsubcategoryList)
        },
        error => {
        }
      );
  }

  onSubcategoryChange(value: any): void {
    if (value) {
      this.bodydisabledSatatus = false;
    }
  }



  reset(){

  }




  ngOnInit(): void {
    this.dropdownloader = true
    let ip_port: any

  this.getLogedInUser()

    ip_port = this.getLocalStoreApi()
    
    this.setApilist(ip_port)
    // this.getTemplateDetail()
    this.getAccountModule()
    this.getTemplateDetailMultiple()
    this.getTemplateDetailSingle()
    
    
    
  }

  resetAll() {
    // Your logic here
  }

  handleSelectTypeChange() {
    // Your logic here
  }
  
  onCheckboxChange(option: string, event: any) {
    if (event.checked) {
      this.selectedOptions[option] = true;
    } else {
      delete this.selectedOptions[option];
    }
    this.resetAll();
    this.handleSelectTypeChange();
  }

  selectedPanel: string = '';

  onRadioChange(panelName: string) {
    this.selectedPanel = panelName;
  }

  submitx(){
    const selectedValues = Object.keys(this.selectedOptions).filter(key => this.selectedOptions[key]);
    console.log("Selected options:", selectedValues);
  }
  submity(){
    const selectedValues = Object.keys(this.selectedOptions3).filter(key => this.selectedOptions3[key]);
    console.log("Selected options:", selectedValues);
  }
// for multimodel
  selectedCategories3: { [key: string]: boolean } = {};
  
  onCheckboxChange3(option: string, event: any) {
    if (event.checked) {
      this.selectedCategories3[option] = true;
    } else {
      delete this.selectedCategories3[option];
    }
  }
  // for 
  selectedCategories2: { [key: string]: boolean } = {};

  onCheckboxChange2(option: string, event: any) {
    if (event.checked) {
      this.selectedCategories2[option] = true;
    } else {
      delete this.selectedCategories2[option];
    }
  }

  oncheckboxChangeCategory(){
    const selectedValues = Object.keys(this.selectedCategories2).filter(key => this.selectedCategories2[key]);
    console.log("Selected options:", selectedValues);
  }
  isDisabled(option: string): boolean {
    const selectedValues = Object.keys(this.selectedCategories2).filter(key => this.selectedCategories2[key]);
    return !selectedValues.includes(option);
  }

}
