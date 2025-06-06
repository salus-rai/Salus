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
import { Component, ViewChild } from '@angular/core';
import { AbstractControl, FormBuilder, FormControl, FormGroup, UntypedFormBuilder, ValidationErrors, Validators } from '@angular/forms';
import { MatOption } from '@angular/material/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSelect } from '@angular/material/select';
import { MatSnackBar } from '@angular/material/snack-bar';
import { PagingConfig } from 'src/app/_models/paging-config.model';
import { NonceService } from 'src/app/nonce.service';
import { UserValidationService } from 'src/app/services/user-validation.service';

@Component({
  selector: 'app-fm-chat-configuration',
  templateUrl: './fm-chat-configuration.component.html',
  styleUrls: ['./fm-chat-configuration.component.css']
})
export class FMChatConfigurationComponent {

  form!: FormControl;
  createNewEmbeddingsform!: FormGroup;
  constructor(private _fb: UntypedFormBuilder, public _snackBar: MatSnackBar, private https: HttpClient, public dialog: MatDialog,private fb: FormBuilder,private validationService:UserValidationService,public nonceService:NonceService) {
    this.form = new FormControl(null, this.fileSelectedValidator);
    this.formCreation()
    this.pagingConfig = {
      itemsPerPage: this.itemsPerPage,
      currentPage: this.currentPage,
      totalItems: this.totalItems
    }
  }
  selectedEmbeddings: any = []
  listReconList: any = ["hi", "hello"]

  userId: any;




  currentPage: number = 1;
  itemsPerPage: number = 5;
  totalItems: number = 0;

  files: any[] = [];
  demoFile: any[] = [];
  selectedFile: File | any;
  file: File | any;

  pagingConfig: PagingConfig = {} as PagingConfig;

  Admin_uploadFile = ""
  Admin_getFiles = ""
  Admin_setCache = ""
  Admin_getEmbedings = ""
  Admin_LLmExplain_deleteFile = ""
  formBased= false


  fileSelectedValidator(control: AbstractControl): ValidationErrors | null {
    if (control.value == null || control.value.length === 0) {
      return { 'noFileSelected': true };
    }
    return null;
  }

  onFileChange(event: any) {
    const reader = new FileReader();
    reader.onload = (e: any) => {
      const text = e.target.result;
      console.log(text);
    };
    reader.readAsText(event.target.files[0]);
  }

  // Handles file selection, validates the file type, and prepares the file list for upload.
  fileBrowseHandler(imgFile: any) {
    // this.browseFilesLenth = imgFile.target.files.length;
    this.files = [];
    this.demoFile = [];
    this.prepareFilesList(imgFile.target.files);
    this.demoFile = this.files;
    this.file = this.files[0];
     // to validate file SAST
     const allowedTypes = ['application/pdf'];
     for(let i =0; i< this.files.length; i++){
       if (!allowedTypes.includes(this.files[i].type)) {
        alert('Please upload a valid file');
         this.files = [];
         this.demoFile = [];
         this.file = '';
         return ;
       }
     }
    this.form.setValue(this.files);
    // this.uploadDocument(this.file);
    //  console.log("on choosing")
  }

  prepareFilesList(files: Array<any>) {
    for (const item of files) {
      // item.progress = 0;
      this.files.push(item);
    }
    this.uploadFilesSimulator(0, this.files);
  }
  // Simulates file upload progress for the selected files.
  uploadFilesSimulator(index: number, files: any) {
    setTimeout(() => {
      console.log(this.files[0].name)
      if (index === this.files.length) {
        return;
      } else {
        this.files[index].progress = 0;
        const progressInterval = setInterval(() => {
          if (this.files[index].progress >= 100) {
            clearInterval(progressInterval);
          } else {
            this.files[index].progress += 10;
          }
        }, 200);
      }
    }, 1000);
  }

  deleteFile() {
    this.files = [];
    this.demoFile = [];
    this.file = null;
  }

  @ViewChild('select1') select1!: MatSelect;

  // SCREEN TWO ADD DATA  
  //--------------VARIABLES-----------embeddigns 

  // selectedReclist: any = [];
  allSelected1: any;
  listShowlist1 = new Set();
  allSelectedInput = false;
  event1: any;
  c1: boolean = false;

  // select 1 -  Toggles the selection of all options in the first select element.
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


  submit() {
    console.log('Form Submitted');
    this.formBased = true
    this.upload_file()
    
  }
  submit2() {
    if (this.createNewEmbeddingsform.valid) {
      this.formBased = true
      // Handle the form submission
    
    console.log('Form Submitted');
    let name = this.createNewEmbeddingsform.value.embeddingName
    let list = this.createNewEmbeddingsform.value.selectedEmbeddings
    
    // console.log("list value",name)
    //   console.log("list value",list)

    this.setcache(name ,list)
    }
  }
  // Sends a POST request to set cache data for embeddings with the provided name and document IDs.
  setcache(name: any, list: any) {
    
      console.log("list value",name)
      console.log("list value",list)
  
      let userIdvalue = this.getLogedInUser()
      let body = new URLSearchParams();
      body.set('userId', userIdvalue!.toString());
      body.set('embName', name);
      body.set('docid', list);

      this.https.post(this.Admin_setCache, body,{
      headers: new HttpHeaders().set('Content-Type', 'application/x-www-form-urlencoded')}).subscribe(
        (res: any) => {
          this.formBased = false
          //console.log( res)
          this.getembeddigns()
          this.getFilestList()
        }, error => {
            const message = (error.error && (error.error.detail || error.error.message)) || "The Api has failed"
            const action = "Close"
            this.formBased = false
            this._snackBar.open(message, action, {
              duration: 3000,
              horizontalPosition: 'left',
              panelClass: ['le-u-bg-black'],
            });
  
          
        })
  
    
  }

  ngOnInit(): void {
    let ip_port: any

    let user = this.getLogedInUser()

    ip_port = this.getLocalStoreApi()
    this.setApilist(ip_port)
    this.getembeddigns()
    this.getFilestList()
  }
  getLogedInUser(): any {
    if (window && window.localStorage && typeof localStorage !== 'undefined') {
      const x = localStorage.getItem("userid") ? JSON.parse(localStorage.getItem("userid")!) : "NA";
      if (x != null && (this.validationService.isValidEmail(x) || this.validationService.isValidName(x))) {
        this.userId = x ;
      }
      console.log("userId", this.userId)
      return this.userId;
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
    this.Admin_uploadFile = ip_port.result.Admin_Rag + ip_port.result.Admin_uploadFile;
    this.Admin_getFiles = ip_port.result.Admin_Rag + ip_port.result.Admin_getFiles;
    this.Admin_setCache = ip_port.result.Admin_Rag + ip_port.result.Admin_setCache;
    this.Admin_getEmbedings = ip_port.result.Admin_Rag + ip_port.result.Admin_getEmbedings;
    this.Admin_LLmExplain_deleteFile = ip_port.result.Admin_Rag + ip_port.result.Admin_LLmExplain_deleteFile;
  }
  dataSource: any = []
  listofDoccuments: any = []
// Fetches the list of uploaded files for the logged-in user.
  getFilestList() {
    let userIdvalue = this.getLogedInUser()
    let body = new URLSearchParams();
    body.set('userId', userIdvalue.toString());
    this.https.post(this.Admin_getFiles, body, {
      headers: new HttpHeaders().set('Content-Type', 'application/x-www-form-urlencoded')
    }).subscribe(
      (res: any) => {
        this.dataSource = res
        this.listofDoccuments = res
      }, error => {
        const message = (error.error && (error.error.detail || error.error.message)) || "The Api has failed"
        const action = "Close"
        this._snackBar.open(message, action, {
          duration: 3000,
          horizontalPosition: 'left',
          panelClass: ['le-u-bg-black'],
        });
      })
  }

  dataSource1: any = []
  // Fetches the list of embeddings for the logged-in user.
  getembeddigns() {
    let userIdvalue = this.getLogedInUser()
    let body = new URLSearchParams();
    body.set('userId', userIdvalue.toString());

    this.https.post(this.Admin_getEmbedings, body, {
      headers: new HttpHeaders().set('Content-Type', 'application/x-www-form-urlencoded')
    }).subscribe(
      (res: any) => {
        this.dataSource1 = res
      }, error => {
          const message = (error.error && (error.error.detail || error.error.message)) || "The Api has failed"
          const action = "Close"
          this._snackBar.open(message, action, {
            duration: 3000,
            horizontalPosition: 'left',
            panelClass: ['le-u-bg-black'],
          });
      })
  }

  formCreation(){
    this.createNewEmbeddingsform = new FormGroup({
      embeddingName: new FormControl('',Validators.required),
      selectedEmbeddings: new FormControl([[], Validators.required])
    });
  }

  upload_file() {
    let userId = this.getLogedInUser()
    const fileData = new FormData();
    this.selectedFile = this.demoFile[0];
      fileData.append('file', this.selectedFile);
      fileData.append('userId', userId)
      this.uploadFileApiCall(fileData)
  
  }
  uploadFileApiCall(fileData: any) {
    this.https.post(this.Admin_uploadFile, fileData).subscribe((res: any) => {
      this.formBased = false
      this.getFilestList()
    }, error => {
      // You can access status:
      console.log(error.status);
        // this.showSpinner1 = false;
        console.log(error)
        this.formBased = false
        const message = (error.error && (error.error.detail || error.error.message)) || "The Api has failed"
        const action = "Close"
        this._snackBar.open(message, action, {
          duration: 3000,
          horizontalPosition: 'left',
          panelClass: ['le-u-bg-black'],
        });

      
    })
  }


  onTableDataChange(event: any) {
    this.currentPage = event;
    this.pagingConfig.currentPage = event;
    this.pagingConfig.totalItems = this.dataSource.length;

  }
  onTableSizeChange(event: any): void {
    this.pagingConfig.itemsPerPage = event.result.value;
    this.pagingConfig.currentPage = 1;
    this.pagingConfig.totalItems = this.dataSource.length;
  }

  // Deletes a file from the database if it is not part of an embedding.
  deleteFileFromDB(status:any,fileId:any){
    // this.fileIdtobedeleted=fileId
    console.log("is cache status",status)
    let userIdvalue = this.getLogedInUser()
    let body = new URLSearchParams();
    body.set('userid', userIdvalue.toString());
    body.set('docid', fileId.toString());
    if(status == "N"){
      // this.https.delete("https://rai-toolkit-rai.az.ad.idemo-ppc.com/api/v1/rai/admin/deleteFile",{body,headers: new HttpHeaders().set('Content-Type', 'application/x-www-form-urlencoded')}).subscribe
      this.https.delete(this.Admin_LLmExplain_deleteFile,{body,headers: new HttpHeaders().set('Content-Type', 'application/x-www-form-urlencoded')}).subscribe
      ((res: any) => {
        if (res.status == "Document Deleted Successfully") {
          const message = "Document Deleted Successfully"
          const action = "Close"
          this._snackBar.open(message, action, {
            duration: 1000,
            panelClass: ['le-u-bg-black'],
          });
        } else {
          const message = "File Deletion was unsucessful"
          const action = "Close"
          this._snackBar.open(message, action, {
            duration: 1000,
            panelClass: ['le-u-bg-black'],
          });

        }

        // this.https.get(this.admin_list_AccountMaping_AccMasterList).subscribe
        this.getFilestList()

      }, error => {
        // You can access status:
        console.log(error.status);
        if (error.status == 430) {
          // this.showSpinner1 = false;
          // this.edited = false;
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
          // this.showSpinner1 = false;
          // this.edited = false;
          // console.log(error.error.detail)
          console.log(error)
          const message = "The Api has failed"
          const action = "Close"
          this._snackBar.open(message, action, {
            duration: 3000,
            horizontalPosition: 'left',
            panelClass: ['le-u-bg-black'],
          });

        }
      })
      
    }else{
      // this.modalservice.open(this.popupview1, { size: 'lg' });
      const message = "This file cannot be deleted as it is a part of the embedding"
      const action = "Close"
      this._snackBar.open(message, action, {
        duration: 3000,
        horizontalPosition: 'left',
        panelClass: ['le-u-bg-black'],
      });
    }
    
  }

  reset(){
    this.files = [];
    this.demoFile = [];
  }


}
