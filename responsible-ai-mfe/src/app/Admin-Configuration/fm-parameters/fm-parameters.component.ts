/**
SPDX-License-Identifier: MIT
Copyright 2024 - 2025 Infosys Ltd.
"
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"
*/ 
import { HttpClient } from '@angular/common/http';
import { Component, Input, ViewChild } from '@angular/core';
import { UntypedFormBuilder, FormGroup, Validators, FormControl } from '@angular/forms';
import { MatOption } from '@angular/material/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSelect } from '@angular/material/select';
import { MatSnackBar } from '@angular/material/snack-bar';
import { NonceService } from 'src/app/nonce.service';

@Component({
  selector: 'app-fm-parameters',
  templateUrl: './fm-parameters.component.html',
  styleUrls: ['./fm-parameters.component.css']
})
export class FmParametersComponent {


  constructor(private _fb: UntypedFormBuilder, public _snackBar: MatSnackBar, private https: HttpClient, public dialog: MatDialog,public nonceService:NonceService) {
    this.fromCreation();
  }

  userId: any;
  FmConfigResponseForm!: FormGroup;

  @Input() parPortfolio!: any;
  @Input() parAccount!: any;


  public recognizerList: any =['PERSON', 'LOCATION', 'DATE', 'AU_ABN', 'AU_ACN', 'AADHAR_NUMBER', 'AU_MEDICARE', 'AU_TFN', 'CREDIT_CARD', 'CRYPTO', 'DATE_TIME', 'EMAIL_ADDRESS', 'ES_NIF', 'IBAN_CODE', 'IP_ADDRESS', 'IT_DRIVER_LICENSE', 'IT_FISCAL_CODE', 'IT_IDENTITY_CARD', 'IT_PASSPORT', 'IT_VAT_CODE', 'MEDICAL_LICENSE', 'PAN_Number', 'PHONE_NUMBER', 'SG_NRIC_FIN', 'UK_NHS', 'URL', 'PASSPORT', 'US_ITIN', 'US_PASSPORT', 'US_SSN'];


  // 
  admin_list_rec_get_list = ""
  admin_list_AccountMaping_AccMasterList = ""
  fm_config_entry = ""
  fm_config_entryList = ""
  fm_config_dataList = ""
  fm_config_dataUpdate = ""
  fm_config_delete = ""
  fm_config_modCheck = ""
  fm_config_topicList = ""
  fm_config_outputModCheck = ""

// Initializes the form group with default values and validators for FM configuration.
  fromCreation() {


    this.FmConfigResponseForm = new FormGroup({
      inputModChecks: new FormControl([], [Validators.required]),
      outputModChecks: new FormControl([], [Validators.required]),
      PromptInjectionThreshold: new FormControl(7, [Validators.required]),
      JailbreakThreshold: new FormControl(7, [Validators.required]),
   //   recognizerNamesToDetect: new FormControl([], [Validators.required]),
      recognizerNamesToBlock: new FormControl([], [Validators.required]),
      RefusalThreshold: new FormControl(7, [Validators.required]),
      ToxicityThreshold: new FormControl(6, [Validators.required]),
      SevereToxicityThreshold: new FormControl(6, [Validators.required]),
      ObsceneThreshold: new FormControl(6, [Validators.required]),
      ThreatThreshold: new FormControl(6, [Validators.required]),
      InsultThreshold: new FormControl(6, [Validators.required]),
      IdentityAttackThreshold: new FormControl(6, [Validators.required]),
      SexualExplicitThreshold: new FormControl(6, [Validators.required]),
      ProfanityCountThreshold: new FormControl(10, [Validators.required]),
      RestrictedtopicThreshold: new FormControl(7, [Validators.required]),
      Restrictedtopics: new FormControl([], [Validators.required]),
      ThemeName: new FormControl('', [Validators.required]),
      Themethresold: new FormControl(6, [Validators.required]),
      ThemeTexts: new FormControl('', [Validators.required]),
    });

    // let initialFormValues = {
    //   account: '',
    //   portfolio: '',
    //   temperature: '',
    //   textDesc: '',
    //   inputModChecks: [],
    //   outputModChecks: [],
    //   PromptInjectionThreshold: 0.7,
    //   JailbreakThreshold: 0.7,
    //   recognizerNamesToDetect: [],
    //   recognizerNamesToBlock: [],
    //   RefusalThreshold: 0.7,
    //   ToxicityThreshold: 0.6,
    //   SevereToxicityThreshold: 0.6,
    //   ObsceneThreshold: 0.6,
    //   ThreatThreshold: 0.6,
    //   InsultThreshold: 0.6,
    //   IdentityAttackThreshold: 0.6,
    //   SexualExplicitThreshold: 0.6,
    //   ProfanityCountThreshold: 1,
    //   RestrictedtopicThreshold: 0.6,
    //   Restrictedtopics: [],
    //   ThemeName: '',
    //   Themethresold: 0.6,
    //   ThemeTexts: '',
    // };


  }

  submit() {
    console.log('Form Submitted');
    console.log('Form Submitted', this.FmConfigResponseForm.value);
    let themeTextArray=[]
    if(this.FmConfigResponseForm.value.ThemeTexts){
      const theme = this.FmConfigResponseForm.value.ThemeTexts;
        themeTextArray = theme!.split(/[,]/);
      }
  
      const ToxicityThreshold = {
        ToxicityThreshold: this.FmConfigResponseForm.value.ToxicityThreshold / 10,
        SevereToxicityThreshold: this.FmConfigResponseForm.value.SevereToxicityThreshold / 10,
        ObsceneThreshold: this.FmConfigResponseForm.value.ObsceneThreshold / 10,
        ThreatThreshold: this.FmConfigResponseForm.value.ThreatThreshold / 10,
        InsultThreshold: this.FmConfigResponseForm.value.InsultThreshold / 10,
        IdentityAttackThreshold: this.FmConfigResponseForm.value.IdentityAttackThreshold / 10,
        SexualExplicitThreshold: this.FmConfigResponseForm.value.SexualExplicitThreshold / 10,
      };
      const RestrictedtopicDetail = {
        RestrictedtopicThreshold: this.FmConfigResponseForm.value.RestrictedtopicThreshold / 10,
        Restrictedtopics: this.FmConfigResponseForm.value.Restrictedtopics,
      };
      const CustomTheme = {
        Themename: this.FmConfigResponseForm.value.ThemeName,
        Themethresold: this.FmConfigResponseForm.value.Themethresold / 10,
        ThemeTexts: themeTextArray,
      };
      const payload1 = {
        PromptinjectionThreshold: this.FmConfigResponseForm.value.PromptInjectionThreshold / 10,
        JailbreakThreshold: this.FmConfigResponseForm.value.JailbreakThreshold / 10,
        PiientitiesConfiguredToDetect: [],
        PiientitiesConfiguredToBlock: this.FmConfigResponseForm.value.recognizerNamesToBlock,
        RefusalThreshold: this.FmConfigResponseForm.value.RefusalThreshold / 10,
        ToxicityThresholds: ToxicityThreshold,
        ProfanityCountThreshold: this.FmConfigResponseForm.value.ProfanityCountThreshold / 10,
        RestrictedtopicDetails: RestrictedtopicDetail,
        CustomTheme: CustomTheme,
      };

      const payload = {
        "AccountName": this.parAccount,
        "PortfolioName": this.parPortfolio,
        "ModerationChecks":this.FmConfigResponseForm.value.inputModChecks,
        "OutputModerationChecks":this.FmConfigResponseForm.value.outputModChecks,
        "ModerationCheckThresholds": payload1
        }

    this.setFMConfigData(payload);

  }
  //  Sends a POST request to save FM configuration data and handles the response or errors.
  setFMConfigData(payload: any) {
    this.https.post(this.fm_config_entry,payload).subscribe(
      (res:any) =>{
        
        const message = 'The Api has succeeded';
        
          const action = 'Close';
          this._snackBar.open(message, action, {
            duration: 3000,
            horizontalPosition: 'left',
            panelClass: ['le-u-bg-black'],
          });
      },
      error => {
        // You can access status:
        console.log(error.status);
        
          
          // console.log(error.error.detail)
          console.log(error);
          const message = 'The Api has failed';
          const action = 'Close';
        
          this._snackBar.open(message, action, {
            duration: 3000,
            horizontalPosition: 'left',
            panelClass: ['le-u-bg-black'],
          });
        }
    )
  }

  ngOnInit(): void {
    let ip_port: any

    let user = this.getLogedInUser()

    ip_port = this.getLocalStoreApi()
    this.setApilist(ip_port)
    this.getSelectDRopDownArrray()
  }
  getLogedInUser() {
    if (localStorage.getItem("userid") != null) {
      const x = localStorage.getItem("userid")
      if (x != null) {

        this.userId = JSON.parse(x)
        console.log(" userId", this.userId)
        return JSON.parse(x)
      }

      console.log("userId", this.userId)
    }
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

    this.admin_list_rec_get_list = ip_port.result.Admin + ip_port.result.Admin_DataRecogGrplist;
    this.admin_list_AccountMaping_AccMasterList = ip_port.result.Admin + ip_port.result.Admin_AccMasterList
    this.fm_config_entry = ip_port.result.Admin + ip_port.result.Fm_Config_Entry;
    this.fm_config_entryList = ip_port.result.Admin + ip_port.result.Fm_Config_EntryList
    this.fm_config_dataList = ip_port.result.Admin + ip_port.result.Fm_Config_Data
    this.fm_config_dataUpdate = ip_port.result.Admin + ip_port.result.Fm_Config_DataUpdate
    this.fm_config_delete = ip_port.result.Admin + ip_port.result.Fm_Config_Delete
    this.fm_config_modCheck = ip_port.result.Admin + ip_port.result.Fm_Config_ModCheck
    this.fm_config_topicList = ip_port.result.Admin + ip_port.result.Fm_Config_TopicList
    this.fm_config_outputModCheck = ip_port.result.Admin + ip_port.result.Fm_Config_OutputModCheck

  }

  @ViewChild('select1') select1!: MatSelect;

  // SCREEN TWO ADD DATA  
  //--------------VARIABLES-----------SECURITY
  selectedApplicableAttack: any;
  applicableAttack: any = [];
  allSelected1: any;
  listShowlist1 = new Set();
  allSelectedInput = false;
  event1: any;
  c1: boolean = false;

  // select 1 - Toggles the selection of all options in the first select element.
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

  // Updates the selection status of the first select element based on selected options.
  selectInputModeration() {
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
  // 

  @ViewChild('select2') select2!: MatSelect;

  // SCREEN TWO ADD DATA  
  //--------------VARIABLES-----------Output mOderation
  allSelected2: any;
  listShowlist2 = new Set();
  allSelectedInput2 = false;
  event2: any;
  c2: boolean = false;

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
  selectOutputModeration() {
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
  // 
  @ViewChild('select3') select3!: MatSelect;

  // SCREEN TWO ADD DATA  
  //--------------VARIABLES-----------selectrecognizerList 
  allSelected3: any;
  listShowlist3 = new Set();
  allSelectedInput3 = false;
  event3: any;
  c3: boolean = false;

  // select 3
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
  selectrecognizerList() {
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

  // 
  @ViewChild('select4') select4!: MatSelect;

  // SCREEN TWO ADD DATA  
  //--------------VARIABLES-----------selectrecognizerListtoblock 
  allSelected4: any;
  listShowlist4 = new Set();
  allSelectedInput4 = false;
  event4: any;
  c4: boolean = false;

  // select 4
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
  selectrecognizerListtoblock() {
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
  // 
  @ViewChild('select5') select5!: MatSelect;

  // SCREEN TWO ADD DATA  
  //--------------VARIABLES-----------selectrecognizerListtoblock 
  allSelected5: any;
  listShowlist5 = new Set();
  allSelectedInput5 = false;
  event5: any;
  c5: boolean = false;

  // select 5
  toggleAllSelection5(event: any) {
    this.event5 = event;
    this.c5 = event.checked;
    this.allSelected5 = !this.allSelected5;
    if (this.allSelected5) {
      this.select5.options.forEach((item: MatOption) => {
        item.select();
        this.listShowlist5.add(item.value);
        const element = document.querySelector('[role="listbox"]');
        if (element instanceof HTMLElement) {
          element.style.display = 'none';
        }
        this.select5.close();
      });
    } else {
      this.select4.options.forEach((item: MatOption) => {
        item.deselect();

        this.listShowlist5.delete(item.value);
      });
    }
  }
  selectRestrictedtopics() {
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

  OutputModerationChecks: any = [];
  Restrictedtopics: any = [];
  InputModerationChecks: any = [];
  // Fetches dropdown data for input moderation, restricted topics, and output moderation checks.
  getSelectDRopDownArrray() {
    this.https.get(this.fm_config_modCheck).subscribe(
      (res: any) => {
        this.InputModerationChecks = res.dataList;
        // this.getAccountMasterEntryList();



      },
      error => {
        // You can access status:
        console.log(error.status);
        if (error.status == 430) {


          console.log(error.error.detail);
          console.log(error);
          const message = error.error.detail;

          const action = 'Close';
          this._snackBar.open(message, action, {
            duration: 3000,
            horizontalPosition: 'left',
            panelClass: ['le-u-bg-black'],
          });
        } else {
          // console.log(error.error.detail)
          console.log(error);
          const message = 'The Api has failed';
          const action = 'Close';
          this._snackBar.open(message, action, {
            duration: 3000,
            horizontalPosition: 'left',
            panelClass: ['le-u-bg-black'],
          });
        }
      }
    );


    this.https.get(this.fm_config_topicList).subscribe(
      (res: any) => {
        this.Restrictedtopics = res.dataList;
      })

    this.https.get(this.fm_config_outputModCheck).subscribe(
      (res: any) => {
        this.OutputModerationChecks = res.dataList;
      })
  }



}
