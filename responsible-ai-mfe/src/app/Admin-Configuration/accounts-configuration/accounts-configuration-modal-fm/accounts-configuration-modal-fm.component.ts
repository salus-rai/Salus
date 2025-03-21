/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { HttpClient } from '@angular/common/http';
import { Component, Inject, ViewChild } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { MatOption } from '@angular/material/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatSelect } from '@angular/material/select';
import { MatSnackBar } from '@angular/material/snack-bar';
import { NonceService } from 'src/app/nonce.service';

@Component({
  selector: 'app-accounts-configuration-modal-fm',
  templateUrl: './accounts-configuration-modal-fm.component.html',
  styleUrls: ['./accounts-configuration-modal-fm.component.css']
})
export class AccountsConfigurationModalFmComponent {
  constructor(public dialogRef: MatDialogRef<AccountsConfigurationModalFmComponent>, public _snackBar: MatSnackBar, public https: HttpClient,public nonceService:NonceService
    , @Inject(MAT_DIALOG_DATA) public data: { id: any }) {
    this.fromCreation();
  }

  autoTicks = false;
  disabled = false;
  // invert = false;
  max = 1;
  min = 0;
  showTicks = true;
  step = 0.1;
  thumbLabel = true;



  dataSource1: any = []
  closeDialog() {
    this.dialogRef.close();
  }

  userId: any

  ngOnInit(): void {
    console.log(this.data)

    
    let ip_port: any

    let user = this.getLogedInUser()

    ip_port = this.getLocalStoreApi()
    this.setApilist(ip_port)
    this.getSelectDRopDownArrray()
    this.get_fmdataforFmConfigResponseform()
    this.recognizerList = ['PERSON', 'LOCATION', 'DATE', 'AU_ABN', 'AU_ACN', 'AADHAR_NUMBER', 'AU_MEDICARE', 'AU_TFN', 'CREDIT_CARD', 'CRYPTO', 'DATE_TIME', 'EMAIL_ADDRESS', 'ES_NIF', 'IBAN_CODE', 'IP_ADDRESS', 'IT_DRIVER_LICENSE', 'IT_FISCAL_CODE', 'IT_IDENTITY_CARD', 'IT_PASSPORT', 'IT_VAT_CODE', 'MEDICAL_LICENSE', 'PAN_Number', 'PHONE_NUMBER', 'SG_NRIC_FIN', 'UK_NHS', 'URL', 'PASSPORT', 'US_ITIN', 'US_PASSPORT', 'US_SSN'];
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

  submit() {
    console.log(this.FmConfigResponseForm.value);

    let themeTextArray=[]
    if(this.FmConfigResponseForm.value.ThemeTexts){
      const theme = this.FmConfigResponseForm.value.ThemeTexts;
        themeTextArray = theme!.split(/[,]/);
      }
   
     const ToxicityThreshold = {
       ToxicityThreshold: this.FmConfigResponseForm.value.ToxicityThreshold,
       SevereToxicityThreshold: this.FmConfigResponseForm.value.SevereToxicityThreshold,
       ObsceneThreshold: this.FmConfigResponseForm.value.ObsceneThreshold,
       ThreatThreshold: this.FmConfigResponseForm.value.ThreatThreshold,
       InsultThreshold: this.FmConfigResponseForm.value.InsultThreshold,
       IdentityAttackThreshold: this.FmConfigResponseForm.value.IdentityAttackThreshold,
       SexualExplicitThreshold: this.FmConfigResponseForm.value.SexualExplicitThreshold,
     };
     const RestrictedtopicDetail = {
       RestrictedtopicThreshold: this.FmConfigResponseForm.value.RestrictedtopicThreshold,
       Restrictedtopics: this.FmConfigResponseForm.value.Restrictedtopics,
     };
     
     const CustomTheme = {
       Themename: this.FmConfigResponseForm.value.ThemeName,
       Themethresold: this.FmConfigResponseForm.value.Themethresold,
       ThemeTexts: themeTextArray
       
       
    
       
    
     };
     const payload1 = {
       PromptinjectionThreshold: this.FmConfigResponseForm.value.PromptInjectionThreshold,
       JailbreakThreshold: this.FmConfigResponseForm.value.JailbreakThreshold,
       PiientitiesConfiguredToDetect: this.FmConfigResponseForm.value.recognizerNamesToDetect,
       PiientitiesConfiguredToBlock: this.FmConfigResponseForm.value.recognizerNamesToBlock,
       RefusalThreshold: this.FmConfigResponseForm.value.RefusalThreshold,
       ToxicityThresholds: ToxicityThreshold,
       ProfanityCountThreshold: this.FmConfigResponseForm.value.ProfanityCountThreshold,
       RestrictedtopicDetails: RestrictedtopicDetail,
       CustomTheme: CustomTheme,
     };
       const payload =
         {
         "accMasterId": this.data.id,
         "ModerationChecks":this.FmConfigResponseForm.value.inputModChecks,
         "OutputModerationChecks":this.FmConfigResponseForm.value.outputModChecks,
         "ModerationCheckThresholds": payload1
         }
         console.log("payload======",payload)
         this.https.patch(this.fm_config_dataUpdate,payload).subscribe(
           (res:any) =>{
             const message = 'FM Parameters has been updated successfully';
               const action = 'Close';
               this._snackBar.open(message, action, {
                 duration: 3000,
                 horizontalPosition: 'left',
                 panelClass: ['le-u-bg-black'],
               });
           },
           error => {
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
         )
   }

  FmConfigResponseForm!: FormGroup;

  fromCreation() {


    this.FmConfigResponseForm = new FormGroup({
      inputModChecks: new FormControl([], [Validators.required]),
      outputModChecks: new FormControl([], [Validators.required]),
      PromptInjectionThreshold: new FormControl(7, [Validators.required]),
      JailbreakThreshold: new FormControl(0.7, [Validators.required]),
      recognizerNamesToDetect: new FormControl([], [Validators.required]),
      recognizerNamesToBlock: new FormControl([], [Validators.required]),
      RefusalThreshold: new FormControl(0.7, [Validators.required]),
      ToxicityThreshold: new FormControl(0.6, [Validators.required]),
      SevereToxicityThreshold: new FormControl(6, [Validators.required]),
      ObsceneThreshold: new FormControl(0.6, [Validators.required]),
      ThreatThreshold: new FormControl(0.6, [Validators.required]),
      InsultThreshold: new FormControl(0.6, [Validators.required]),
      IdentityAttackThreshold: new FormControl(0.6, [Validators.required]),
      SexualExplicitThreshold: new FormControl(0.6, [Validators.required]),
      ProfanityCountThreshold: new FormControl(0.10, [Validators.required]),
      RestrictedtopicThreshold: new FormControl(0.6, [Validators.required]),
      Restrictedtopics: new FormControl([], [Validators.required]),
      ThemeName: new FormControl('', [Validators.required]),
      Themethresold: new FormControl(0.6, [Validators.required]),
      ThemeTexts: new FormControl('', [Validators.required]),
    });

  

  }
  // 
  InputModerationChecks:any = []
  OutputModerationChecks:any = []
  recognizerList:any = []
  Restrictedtopics:any = []


  // 
  // 
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

  // select 1
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

  dataSource3: any;

  get_fmdataforFmConfigResponseform() {
    this.https.post(this.fm_config_dataList, { accMasterId: this.data.id }).subscribe
      ((res: any) => {
        if(res==null){
          const message = 'FM Parameters is not set for this account';
          const action = 'Close';
          this._snackBar.open(message, action, {
            duration: 3000,
            horizontalPosition: 'left',
            panelClass: ['le-u-bg-black'],
          });
        }
        this.dataSource3 = res.dataList[0];
          this.FmConfigResponseFormSETformValues(this.dataSource3)
   
      }, error => {
        console.log(error.status);
        if (error.status == 430) {
          console.log(error.error.detail)
          console.log(error)
          const message = error.error.detail
          const action = "Close"
          this._snackBar.open(message, action, {
            duration: 3000,
            horizontalPosition: 'left',
            panelClass: ['le-u-bg-black'],
          });
        } else {
          console.log(error)
          const message = "The Api has failed"
          // this.getAccountMasterEntryList()
          const action = "Close"
          this._snackBar.open(message, action, {
            duration: 3000,
            horizontalPosition: 'left',
            panelClass: ['le-u-bg-black'],
          });
  
        }
      })
  }
  FmConfigResponseFormSETformValues(dataSource3: any) {
    this.FmConfigResponseForm.get('inputModChecks')?.setValue(dataSource3?.ModerationChecks)
    this.FmConfigResponseForm.get('outputModChecks')?.setValue(dataSource3?.OutputModerationChecks)
    this.FmConfigResponseForm.get('PromptInjectionThreshold')?.setValue(dataSource3?.ModerationCheckThresholds?.PromptinjectionThreshold)
    this.FmConfigResponseForm.get('JailbreakThreshold')?.setValue(dataSource3?.ModerationCheckThresholds?.JailbreakThreshold)
    this.FmConfigResponseForm.get('recognizerNamesToDetect')?.setValue(dataSource3?.ModerationCheckThresholds?.PiientitiesConfiguredToDetect)
    this.FmConfigResponseForm.get('recognizerNamesToBlock')?.setValue(dataSource3?.ModerationCheckThresholds?.PiientitiesConfiguredToBlock)
    this.FmConfigResponseForm.get('RefusalThreshold')?.setValue(dataSource3?.ModerationCheckThresholds?.RefusalThreshold)
    this.FmConfigResponseForm.get('ToxicityThreshold')?.setValue(dataSource3?.ModerationCheckThresholds?.ToxicityThresholds?.ToxicityThreshold)
    this.FmConfigResponseForm.get('SevereToxicityThreshold')?.setValue(dataSource3?.ModerationCheckThresholds?.ToxicityThresholds?.SevereToxicityThreshold)
    this.FmConfigResponseForm.get('ObsceneThreshold')?.setValue(dataSource3?.ModerationCheckThresholds?.ToxicityThresholds?.ObsceneThreshold)
    this.FmConfigResponseForm.get('ThreatThreshold')?.setValue(dataSource3?.ModerationCheckThresholds?.ToxicityThresholds?.ThreatThreshold)
    this.FmConfigResponseForm.get('InsultThreshold')?.setValue(dataSource3?.ModerationCheckThresholds?.ToxicityThresholds?.InsultThreshold)
    this.FmConfigResponseForm.get('IdentityAttackThreshold')?.setValue(dataSource3?.ModerationCheckThresholds?.ToxicityThresholds?.IdentityAttackThreshold)
    this.FmConfigResponseForm.get('SexualExplicitThreshold')?.setValue(dataSource3?.ModerationCheckThresholds?.ToxicityThresholds?.SexualExplicitThreshold)
    this.FmConfigResponseForm.get('ProfanityCountThreshold')?.setValue(dataSource3?.ModerationCheckThresholds?.ProfanityCountThreshold)
    this.FmConfigResponseForm.get('RestrictedtopicThreshold')?.setValue(dataSource3?.ModerationCheckThresholds?.RestrictedtopicDetails?.RestrictedtopicThreshold)
    this.FmConfigResponseForm.get('Restrictedtopics')?.setValue(dataSource3?.ModerationCheckThresholds?.RestrictedtopicDetails?.Restrictedtopics)
    this.FmConfigResponseForm.get('ThemeName')?.setValue(dataSource3?.ModerationCheckThresholds?.CustomTheme?.Themename)
    this.FmConfigResponseForm.get('Themethresold')?.setValue(dataSource3?.ModerationCheckThresholds?.CustomTheme?.Themethresold)
    this.FmConfigResponseForm.get('ThemeTexts')?.setValue(dataSource3?.ModerationCheckThresholds?.CustomTheme?.ThemeTexts)
  }
  // 

  // set the value of the form in base 
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