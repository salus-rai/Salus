/**
SPDX-License-Identifier: MIT
Copyright 2024 - 2025 Infosys Ltd.
"
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"
*/ 
import { Component, ViewEncapsulation } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { PagingConfig } from 'src/app/_models/paging-config.model';
import { FormBuilder } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatDialog } from '@angular/material/dialog';
import { PageRoleAccessComponent } from './page-role-access/page-role-access.component';
@Component({
  selector: 'app-user-management',
  templateUrl: './user-management.component.html',
  styleUrls: ['./user-management.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class UserManagementComponent {
  searchQuery: string = '';
  filteredItems: string[] = [];
  isSearchOpen: boolean = false;
  filteredUsers:any;

  // for role-access
  accessiblePages : any;
  //
  currentPage: number = 1;
  itemsPerPage: number = 5;
  totalItems: number = 0;
  pagingConfig: PagingConfig = {} as PagingConfig;


  users = [
    {name: 'John Doe', email: 'john.doe@example.com'},
    {name: 'Jane Doe', email: 'jane.doe@example.com'},
    // more users here
  ];
  dataSource :any =[]
  editIndex: number[] = [];

    Backend_Users = ""
    Backend_authorities = ""
    Backend_UpdateUser = ""
    Backend_DeleteUser = ""

    userId: any;


  edit(i: any,u:any) {
    this.editIndex.push(i);
    if (u == true) {
      this.showActivationStatus = "User Activated";
    } else {
      this.showActivationStatus = "User Deactivated";
    }
  }

  // Updates the user's activation status and authorities, then sends the updated data to the backend.
  update(i: any,id:any,activated:any,authorities:any) {
    this.editIndex = this.editIndex.filter(index => index !== i);
    // Here you can also add the logic to update the user in your backend
    console.log("activated",activated);
    console.log("authorities",authorities);
    let header = {
      "activated": activated,
      "authorities":authorities,
      "id": id
    }

    this.updateUser(header);
  }
  //
  // ...

  constructor(private https: HttpClient,private fb: FormBuilder,public _snackBar: MatSnackBar
    , public dialog: MatDialog) {
    this.pagingConfig = {
      itemsPerPage: this.itemsPerPage,
      currentPage: this.currentPage,
      totalItems: this.totalItems
    }
  }
  ngOnInit() {
    let ip_port: any

    let user = this.getLogedInUser()

    ip_port = this.getLocalStoreApi()
    this.setApilist(ip_port)
    this.getUserData();
    this.getListofAuthorities();
  }

  openDialog() {
    console.log(this.accessiblePages, "accessiblePages")
    // console.log(this.Backend_Users , "Backend_Users")
    this.dialog.open(PageRoleAccessComponent, {
      // width: '52vw',
      // height: 'calc(100vh - 57px)', // Subtract the height of the navbar
      position: {
        top: '57px', // Position the modal below the navbar
        right: '0'
      },
      backdropClass: 'custom-backdrop',
      data: {
        options: this.options,
        accessiblePagesUrl: this.accessiblePages.replace('.com:', '.com')
      }
      // height: '400px',
      // width: '800px'
    });
  }

search() {
    if (this.searchQuery) {
      this.filteredUsers = this.dataSource.userList.filter((user: { firstName: string; }) =>
        user.firstName.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
      console.log(this.filteredUsers, "Users Filtered")
    } else {
      this.filteredUsers = this.dataSource.userList;
    }
    console.log(this.dataSource, "Users from backend")
  }

  closeSearch() {
    this.isSearchOpen = false;
    this.searchQuery = '';
    this.filteredUsers = this.dataSource.userList;
  }

toggleSearch() {
  this.isSearchOpen = !this.isSearchOpen;
  this.searchQuery = '';
  this.filteredItems = [];
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
    // ip_port.result.Backend = "http://localhost:30019"
    this.accessiblePages = ip_port.result.Backend
    this.Backend_Users = ip_port.result.Backend + ip_port.result.Backend_Users
    this.Backend_authorities = ip_port.result.Backend + ip_port.result.Backend_authorities
    this.Backend_UpdateUser = ip_port.result.Backend + ip_port.result.Backend_UpdateUser
    this.Backend_DeleteUser = ip_port.result.Backend + ip_port.result.Backend_DeleteUser
  }
  getUserData() {
    this.https.get(this.Backend_Users).subscribe(
      (response: any) => {
        // Handle successful response here
        console.log(response);
        this.dataSource = response;
        this.filteredUsers = this.dataSource.userList;
      },
      (error: HttpErrorResponse) => {
      }
    );
  }
  onTableDataChange(event: any) {
    this.currentPage = event;
    this.pagingConfig.currentPage = event;
    this.pagingConfig.totalItems = this.dataSource.length;
  }
  selectedValues: string[] = ['1', '2']; // pre-selected values
options = [];

getListofAuthorities() {
  this.https.get(this.Backend_authorities).subscribe((res:any)=>{
    console.log(res);
    this.options = res;
  })
  }

  // Deletes a user by their ID and refreshes the user list upon success.
  clickDeleteUser(id: any) {
    let x = this.Backend_DeleteUser
    let y = `${x}/delete?id=${id}`
    // console.log("http://10.66.155.13:30019/v1/rai/backend/users/delete?id="+id+"");
    this.https.delete(y).subscribe({
      next: (response:any) => {
        console.log('User deleted successfully', response);
        this.getUserData();
        if (response[1] == 204) {


          const message = "User Deleted Successfully"
          const action = "Close"
          this._snackBar.open(message, action, {
            duration: 1000,
            panelClass: ['le-u-bg-black'],
          });
        } else if (response.status != 204) {
          const message = "User Deletion was unsucessful"
          const action = "Close"
          this._snackBar.open(message, action, {
            duration: 1000,
            panelClass: ['le-u-bg-black'],
          });

        }
        // Optionally, refresh the list of users or authorities here
      },
      error: (error) => {
      }
    });
  }

  // Returns and sets the activation status message based on the user's activation state.
  showActivationStatus:any;
  userActivatedValue(value: any) {
    // console.log(value);
    if(value == true){
      this.showActivationStatus = "User Activated"
      return this.showActivationStatus = "User Activated";
    }else{
      this.showActivationStatus ="User Deactivated"
      return this.showActivationStatus ="User Deactivated";
    }
  }

  // Logs and updates the activation status message when the activation toggle is changed.
  ontoggleOpen(event: any, value: any) {
    // console.log("event",event);
    console.log("event", event.target.checked);
    console.log("value",value);
    if(event.target.checked == true){
      this.showActivationStatus = "User Activated"
      console.log("User Activated",this.showActivationStatus);
    }
    else{
      this.showActivationStatus ="User Deactivated"
      console.log("User Deactivated",this.showActivationStatus);
    }
  }

  handleClick(i:any){
    console.log(i);
  }

  // Sends updated user data to the backend and refreshes the user list upon success.
  updateUser(header: any) {
    this.https.patch(this.Backend_UpdateUser, header).subscribe({
      next: (response) => {

        console.log('User updated successfully', response);
        this.getUserData();
      },error: (error) => {
      }
    });
  }

}

