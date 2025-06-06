/**
SPDX-License-Identifier: MIT
Copyright 2024 - 2025 Infosys Ltd.
"
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"
*/ 
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, Inject, ViewChild } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { MatOption } from '@angular/material/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatSelect } from '@angular/material/select';
import { MatSnackBar } from '@angular/material/snack-bar';
import { NgbPopover } from '@ng-bootstrap/ng-bootstrap';
import { PagingConfig } from 'src/app/_models/paging-config.model';
import { NonceService } from 'src/app/nonce.service';

@Component({
  selector: 'app-accounts-configuration-modal-privacy',
  templateUrl: './accounts-configuration-modal-privacy.component.html',
  styleUrls: ['./accounts-configuration-modal-privacy.component.css']
})
export class AccountsConfigurationModalPrivacyComponent {
  constructor(public dialogRef: MatDialogRef<AccountsConfigurationModalPrivacyComponent>, public _snackBar: MatSnackBar, public https: HttpClient,public nonceService:NonceService
    , @Inject(MAT_DIALOG_DATA) public data: { id: any, ThresholdScore: any, }) {
      this.formCreation();
    this.pagingConfig = {
      itemsPerPage: this.itemsPerPage,
      currentPage: this.currentPage,
      totalItems: this.totalItems
    }
  }

  @ViewChild('p') p!: NgbPopover;
  closeToggle(p:any){
  if (this.p.isOpen()) {
    console.log('Popover is open');
    this.p.toggle();
  } else {
    this.p.toggle();
    console.log('Popover is closed');
  }

  
}
  isLoading = false;

  edited: any = false;
  autoTicks = false;
  disabled = false;
  // invert = false;
  max = 1;
  min = 0;
  showTicks = true;
  step = 0.01;
  thumbLabel = true;



  pagingConfig: PagingConfig = {} as PagingConfig;
  currentPage: number = 1;
  itemsPerPage: number = 5;
  totalItems: number = 0


  public resThresholdScore: number = 0;


  dataSource1: any = []
  dataSource2: any = []
  closeDialog() {
    this.dialogRef.close();
  }

  @ViewChild('select1') select1!: MatSelect;

// SCREEN TWO ADD DATA  
//--------------VARIABLES-----------SECURITY

allSelected1: any;
listShowlist1 = new Set();
allSelectedInput = false;
event1: any;
c1: boolean = false;

// select 1 - // toggles the selection of all options in the first select element.
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

// Updates the status of the first select element based on selected options.
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


  ngOnInit(): void {
    this.thresholdDisplay = this.data.ThresholdScore
    this.resThresholdScore = this.data.ThresholdScore
    let ip_port: any
    let user = this.getLogedInUser()

    ip_port = this.getLocalStoreApi()
    this.setApilist(ip_port)
    this.isLoading = true;
    console.log(this.data);


    this.getAccountMasterEntryList()



  }
  userId: any
  // get the user id from the local storage
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
  admin_list_AccountMaping_Acc_PrivacyEncrypt = ""
  admin_list_AccountMaping_Acc_ThresholdUpdate=""
  admin_list_rec_get_list=""
  admin_list_AccountMaping_AccMasterList_Update_Data=""
  admin_list_AccountMaping_AccMasterList_dataList=""
  admin_list_AccountMaping_AccMasterList_Delete_Data=""
  setApilist(ip_port: any) {
    this.admin_list_AccountMaping_Acc_PrivacyEncrypt = ip_port.result.Admin + ip_port.result.Admin_PrivacyEncrypt
    this.admin_list_AccountMaping_Acc_ThresholdUpdate = ip_port.result.Admin + ip_port.result.Admin_ThresholdUpdate
    this.admin_list_rec_get_list = ip_port.result.Admin + ip_port.result.Admin_DataRecogGrplist     
    this.admin_list_AccountMaping_AccMasterList_Update_Data = ip_port.result.Admin + ip_port.result.Admin_AccEntityAdd  
    this.admin_list_AccountMaping_AccMasterList_dataList = ip_port.result.Admin + ip_port.result.Admin_AccDataList
    this.admin_list_AccountMaping_AccMasterList_Delete_Data = ip_port.result.Admin + ip_port.result.Admin_AccDataDelete      
  }

// Updates the active status of a recognizer for the account.
  updateActiveStatus(element: any, RecogId: any) {

    // this.resAccMasterid
    // console.log(element.checked,RecogId,this.resAccMasterid)
    // element.activate = !element.activate;


    this.https.post(this.admin_list_AccountMaping_Acc_PrivacyEncrypt, { accMasterId: this.data.id, dataRecogGrpId: RecogId, isHashify: element.checked }).subscribe
      ((res: any) => {
        if (res.status === "True") {

          const message = "Updated Successfully "
          this.getAccountMasterEntryList()
          const action = "Close"
          this._snackBar.open(message, action, {
            duration: 3000,
            panelClass: ['le-u-bg-black'],
          });
        } else if (res.status === "False") {

          const message = "Data Encryption Removed "
          this.getAccountMasterEntryList()
          const action = "Close"
          this._snackBar.open(message, action, {
            duration: 3000,
            panelClass: ['le-u-bg-black'],
          });

        }

      })

  }
  getAccountMasterEntryList() {
    let payload = {
      accMasterId: this.data.id
    }
    this.https.post(this.admin_list_AccountMaping_AccMasterList_dataList, payload).subscribe((response: any) => {
      console.log(response);
      this.isLoading = false;

      this.dataSource1 = response;
      this.dataSource2 = response.dataList
    });
  }

  public thresholdDisplay: any = 0;

  // Sets and updates the threshold score for the account.
  setThreshold(e: any,valuex:any) {
    this.thresholdDisplay = valuex
    console.log("slide value",valuex)
    // this.showSpinner1 = true;
    this.https.patch(this.admin_list_AccountMaping_Acc_ThresholdUpdate, { accMasterId: this.data.id, thresholdScore: valuex }).subscribe
      ((res: any) => {
        if (res.status === "True") {
          // this.showSpinner1 = false;
          const message = "Threshold Score Updated Successfully "
          const action = "Close"
          this._snackBar.open(message, action, {
            duration: 3000,
            panelClass: ['le-u-bg-black'],
          });

          //
          
          //
        } else if (res.status === "False") {
          // this.showSpinner1 = false;
          const message = "Threshold Score Updation Failed"
          const action = "Close"
          this._snackBar.open(message, action, {
            duration: 3000, panelClass: ['le-u-bg-black']
          });

        }


      }, error => {
        // You can access status:
        console.log(error.status);
        if (error.status == 430) {
          // this.showSpinner1 = false;
          this.edited = false;
          console.log(error.error.detail)
          console.log(error)
          const message = error.error.detail
          const action = "Close"
          this._snackBar.open(message, action, {
            duration: 3000,
            horizontalPosition: 'left',
            panelClass: ['le-u-bg-black']
          });
        } else {
          // this.showSpinner1 = false;
          this.edited = false;
          // console.log(error.error.detail)
          console.log(error)
          const message = "The Api has failed"
          const action = "Close"
          this._snackBar.open(message, action, {
            duration: 3000,
            horizontalPosition: 'left',
            panelClass: ['le-u-bg-black']
          });

        }
      })

      

  }
 
  // Adds a new recognizer to the list by fetching available recognizers and filtering out existing ones.
  editReconList:any[] = []
  addRecognizerInList() {
    this.https.get(this.admin_list_rec_get_list).subscribe
      ((res: any) => {
        this.editReconList = (getDifference(res.RecogList, this.dataSource2));

      }, error => {
        // You can access status:
        console.log(error.status);
        if (error.status == 430) {
          this.edited = false;
          console.log(error.error.detail)
          console.log(error)
          const message = error.error.detail
          // this.getAccountMasterEntryList()
          const action = "Close"
          this._snackBar.open(message, action, {
            duration: 3000,
            horizontalPosition: 'left',
            panelClass: ['le-u-bg-black'],
          });
        } else {
          this.edited = false;
          // console.log(error.error.detail)
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
    function getDifference(array1: any[], array2: any[]) {
      return array1.filter((object1: { RecogId: any; }) => {
        return !array2.some((object2: { RecogId: any; }) => {
          return object1.RecogId === object2.RecogId;
        });
      });
    }
    // this.listShowlist1 = new Set()
   
  }



  getDifference(array1: any[], array2: any[]) {
    return array1.filter((object1: { RecogId: any; }) => {
      return !array2.some((object2: { RecogId: any; }) => {
        return object1.RecogId === object2.RecogId;
      });
    });
  }
   
  // 

  

  accountUpdateForm!: FormGroup;

  formCreation(){
    this.accountUpdateForm = new FormGroup({
      updateRecList: new FormControl([], [Validators.required]),
    });
  }

  // Updates the recognizer list for the account with the selected recognizers.
  updateRecList(){
    console.log("updateRecList")
    console.log(this.accountUpdateForm.value)
    console.log(this.accountUpdateForm.get('listRecognizerNames1')?.value)
    console.log(this.listShowlist1)
    let listShowlist1 = Array.from(this.listShowlist1)
    console.log(listShowlist1)
    let payload = {
      accMasterId: this.data.id,
      dataRecogGrpId: listShowlist1
    }

    this.https.patch(this.admin_list_AccountMaping_AccMasterList_Update_Data, { dataGrpList: this.accountUpdateForm.value.updateRecList, accMasterId: this.data.id }).subscribe
      ((res: any) => {
        console.log("vale updated in " + res.status)
        if (res.status === "True") {
          const message = "New Recognizer Added Successfully"
          const action = "Close"
          this.getAccountMasterEntryList();
          this._snackBar.open(message, action, {
            duration: 1000,
            panelClass: ['le-u-bg-black'],
          });
          this.accountUpdateForm.reset();
        } else if (res.status === "False") {
          const message = "New Recognizer didn't got Added Successfully"
          this.getAccountMasterEntryList()
          const action = "Close"
          this._snackBar.open(message, action, {
            duration: 1000,
            panelClass: ['le-u-bg-black'],
          });

        }
        this.getAccountMasterEntryList()

      }, error => {
        // You can access status:
        console.log(error.status);
        if (error.status == 430) {
          // this.showSpinner1 = false;
          this.edited = false;
          console.log(error.error.detail)
          console.log(error)
          const message = error.error.detail
          this.getAccountMasterEntryList()
          const action = "Close"
          this._snackBar.open(message, action, {
            duration: 3000,
            horizontalPosition: 'left',
            panelClass: ['le-u-bg-black'],
          });
        } else {
          // this.showSpinner1 = false;
          this.edited = false;
          // console.log(error.error.detail)
          console.log(error)
          const message = "The Api has failed"
          this.getAccountMasterEntryList();
          const action = "Close"
          this._snackBar.open(message, action, {
            duration: 3000,
            horizontalPosition: 'left',
            panelClass: ['le-u-bg-black'],
          });

        }
      })
  }

  // Deletes account data for the specified recognizer ID.
  deleteAccounttData(id: any) {

    const options = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
      }),
      body: {
        RecogId: id,
        accMasterId: this.data.id
      },
    };
    this.https.delete(this.admin_list_AccountMaping_AccMasterList_Delete_Data, options).subscribe
      ((res: any) => {
        if (res.status === "True") {
          const message = "Account Data Deleted Successfully"
          const action = "Close"
          this. getAccountMasterEntryList();
          this._snackBar.open(message, action, {
            duration: 1000, panelClass: ['le-u-bg-black'],
          });
        } else if (res.status === "False") {
          const message = "Account Data Deletion was unsucessful"
          this.getAccountMasterEntryList()
          const action = "Close"
          this._snackBar.open(message, action, {
            duration: 1000, panelClass: ['le-u-bg-black'],
          });

        }

       this.getAccountMasterEntryList()

      }, error => {
        // You can access status:
        console.log(error.status);
        if (error.status == 430) {
          this.edited = false;
          console.log(error.error.detail)
          console.log(error)
          const message = error.error.detail
          this.getAccountMasterEntryList()
          const action = "Close"
          this._snackBar.open(message, action, {
            duration: 3000,
            horizontalPosition: 'left',
            panelClass: ['le-u-bg-black'],
          });
        } else {
          // console.log(error.error.detail)
          console.log(error)
          const message = "The Api has failed"
          this.getAccountMasterEntryList()
          const action = "Close"
          this._snackBar.open(message, action, {
            duration: 3000,
            horizontalPosition: 'left',
            panelClass: ['le-u-bg-black'],
          });

        }
      })

      

  }


  onTableDataChange(event: any) {
    this.pagingConfig.currentPage = event;
    this.pagingConfig.totalItems = this.dataSource1.length;
  }
  onTableSizeChange(event: any): void {
    this.pagingConfig.itemsPerPage = event.result.value;
    this.pagingConfig.currentPage = 1;
    this.pagingConfig.totalItems = this.dataSource1.length;
  }




}
