/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { HttpClient } from '@angular/common/http';
import { Component,OnInit } from '@angular/core';
import { AbstractControl, FormControl, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { PagingConfig } from 'src/app/_models/paging-config.model';
import { NonceService } from 'src/app/nonce.service';

@Component({
  selector: 'app-legal-agent',
  templateUrl: './legal-agent.component.html',
  styleUrls: ['./legal-agent.component.css']
})
export class LegalAgentComponent implements OnInit {
  files: any[] = [];
  demoFile: any[] = [];
  file: File | any;
  selectedFile: File | any;
  showSpinner1 = false;
  useCase!: FormGroup;
  dataSource: any = [];
  user:any;
   // FOR SHIMMER LOADING
   isLoadingTable = true;
  // API
  getData: any;
  legalUpload: any;
  // pagination
  pagingConfig: PagingConfig = {} as PagingConfig;
  currentPage: number = 1;
  itemsPerPage: number = 5;
  totalItems: number = 0;
 

  constructor (public _snackBar: MatSnackBar, private https: HttpClient, private snackBar: MatSnackBar,public nonceService:NonceService)
  {
    this.pagingConfig = {
      itemsPerPage: this.itemsPerPage,
      currentPage: this.currentPage,
      totalItems: this.totalItems
    }
    this.useCase = new FormGroup({
      //useCaseName: new FormControl('', [Validators.required]),
      fileData: new FormControl('', [Validators.required]),
    });
  }
  ngOnInit(): void {
    let ip_port: any;
    this.user = localStorage.getItem('userid')?JSON.parse(localStorage.getItem('userid')!) : '';
    ip_port = this.getLocalStoreApi();
    // seting up api list
    this.setApiList(ip_port);
    this.getAllData();
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
  setApiList(ip_port: any) {
    this.getData = ip_port.result.legalAgent + ip_port.result.legalAgentReports ;//"http://10.152.196.184:30080/v1/legalAgent/getAllReports";
    this.legalUpload = ip_port.result.legalAgent + ip_port.result.legalAgentUpload ;//"http://10.152.196.184:30080/v1/legalAgent/uploadFile";

    console.log("this.getData::",this.getData)
  }
// ----------------Pagination-----------------
onTableDataChange(event: any) {
  this.currentPage = event;
  this.pagingConfig.currentPage = event;
  this.pagingConfig.totalItems = this.dataSource.length;
}

  onFileChange(event: any) {
    const reader = new FileReader();
    reader.onload = (e: any) => {
      const text = e.target.result;
    //  console.log(text);
    };
    reader.readAsText(event.target.files[0]);
  }

  fileBrowseHandler(file: any){
    // to validate file SAST
    const allowedTypes = ['application/pdf','text/plain'];
    for(let i =0; i< this.file.length; i++){
      if (!allowedTypes.includes(this.file[i].type)) {
        this._snackBar.open('Please upload valid file', 'Close', {
          duration: 2000,
        });
        this.file = [];
        return ;
      }
    }
    this.prepareFilesList(file.target.files);
    this.demoFile = this.files;
    this.file = this.files[0];
  }
  prepareFilesList(files: Array<any>) {
    this.files = []
    for (const item of files) {
      const cleanedName = item.name.replace(/\[object Object\]/g, '');
      const newFile = new File([item], cleanedName, { type: item.type });
      this.files.push(newFile);
    }
    this.uploadFilesSimulator(0, files)
  }
  uploadFilesSimulator(index: number, files: any) {
    setTimeout(() => {
      if (index === this.files.length) {
        console.log("RETURN")
        return;
      } else {
        this.files[index].progress = 0;
        const progressInterval = setInterval(() => {
          if (this.files[index].progress >= 100) {
            clearInterval(progressInterval);
          } else {
            console.log("ELSE BLOCK")
            this.files[index].progress += 10;
          }
        }, 200);
      }
    }, 1000);
  }
  deleteFile(){
    this.files = [];
    this.demoFile = [];
    this.file = null;
  }
  submit(){
    if (this.useCase.invalid) {
      this.snackBar.open('Please select a File', '✖', {
        horizontalPosition: 'center',
        verticalPosition: 'top',
        duration: 3000,
      });
      return;
    }
    const fileData = new FormData();
    this.selectedFile = this.files[0];
    fileData.append('file', this.selectedFile);
    fileData.append('user_id', this.user);
    this.https.post(this.legalUpload ,fileData).subscribe((res: any)=>{
      this.getAllData();
      const message = res?.message;
      const action = "Close";
      this.snackBar.open(message, action, {
        duration: 3000,
        panelClass: ['le-u-bg-black'],
      });
    }, error => {
      this.showSpinner1 = false;
      const message = (error && error.error && (error.error.detail || error.error.message)) || "The Api has failed"
      const action = "Close"
      this.snackBar.open(message, action, {
        duration: 3000,
        panelClass: ['le-u-bg-black'],
      });
    })
  }
  reset(){
    this.files = [];
    this.demoFile = [];
    this.file = null;
  }
  getErrorMessage(control: AbstractControl): string {
    if (control.hasError('required')) {
      return 'File is required.';
    } else {
      return 'Please enter a valid file.';
    }
  }
  getAllData(){
    //this.getData = this.getData + '?user_id='+ this.user;
    this.https.get(this.getData + '?user_id='+ this.user).subscribe
    ((res: any)=>{
      this.dataSource = res;
      this.onTableDataChange(this.currentPage);
      this.isLoadingTable = false;
    }, error => {
      const message = (error && error.error && (error.error.detail || error.error.message)) || "The Api has failed"
      const action = "Close"
      this.snackBar.open(message, action, {
        duration: 3000,
        panelClass: ['le-u-bg-black'],
      });
    })
  }
  getfileContent(documentLink: string){
    console.log('Navigating to:', documentLink);
    window.location.href = documentLink; 
  }
}
