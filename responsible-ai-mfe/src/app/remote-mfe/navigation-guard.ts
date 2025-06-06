/**
SPDX-License-Identifier: MIT
Copyright 2024 - 2025 Infosys Ltd.
"
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"
*/ 
import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, UrlTree, Router } from '@angular/router';
import { Observable, catchError, map, of, tap } from 'rxjs';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class UsecaseGuard implements CanActivate {
  userId:any;
  getUseCase: any;
  usecaseavailability : any;
  createUseCase: any;
  ip_port:any
  userRole:any;
  userRole1:any;
  constructor(private router: Router,public https: HttpClient) { }

  // Determines if a route can be activated based on user roles and use case availability.
  canActivate(

    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {
    this.ip_port = this.getLocalStoreApi();
    this.setApilist(this.ip_port);
    this.userRole1 = this.getLogedInUserRole();
    console.log("userRole1",this.userRole1)
    return this.checkIfUsecasesAvailable().pipe(
      tap(usecasesAvailable => {
        console.log("usecasesAvailable", usecasesAvailable);
      }),
      map(usecasesAvailable => {
        if (usecasesAvailable || this.userRole1=="ROLE_ML" || this.userRole1=="ROLE_EMPTY" || this.userRole1=="ROLE_ADMIN" ) {
          return true;
        } else {
          this.router.navigate(['/responsible-ui/']);
          return false;
        }
      })
    );
  }

  // Checks if use cases are available for the logged-in user by making an API call.
  checkIfUsecasesAvailable(): Observable<Boolean> {
    const user = this.getLogedInUser();

    console.log("User", user);
    return this.https.get(this.getUseCase + '"' + user + '"').pipe(

      map((res: any) => {
        console.log( "res",res)
        console.log("getUseCase", this.getUseCase);
        // If the response is not empty and useCaseName array is not empty, return true
        if (res && res.length > 0 && res[0].useCaseName && res[0].useCaseName.length > 0) {
          return true;
        }
        // If the response is empty or useCaseName array is empty, return false
        return false;
            }),
            catchError(error => {
              return of(false);
            })
    );

  }

  // Retrieves the logged-in user ID from local storage.
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

  //  Retrieves the logged-in user's role from local storage.
  getLogedInUserRole() {
    if (localStorage.getItem("role") != null) {
      const x = localStorage.getItem("role")
      if (x != null) {

        this.userRole = JSON.parse(x)
        console.log(" USER ROLE", this.userRole)
        return JSON.parse(x)
      }

      console.log("USER ROLE", this.userRole)
    }
  }

// Retrieves API configuration details from local storage.
  getLocalStoreApi() {
    let ip_port
    if (localStorage.getItem("res") != null) {
      const x = localStorage.getItem("res")
      console.log("X********GET LOCAL STORE API",x)
      if (x != null) {
        return ip_port = JSON.parse(x)
      }
    }
  }

  // seting up api list
  setApilist(ip_port: any) {
    // this.getFile = ip_port.result.DocProcess + ip_port.result.DocProcess_getFiles  // + environment.getFile
    // this.uploadFile = ip_port.result.DocProcess + ip_port.result.DocProcess_uploadFile   //+ environment.uploadFile
    // this.DocProcessing_getFileContent = ip_port.result.DocProcess + ip_port.result.DocProcessing_getFileContent   //+ environment.uploadFile
    this.createUseCase =ip_port.result.Questionnaire + ip_port.result.Questionnaire_createUsecase
    this.getUseCase = ip_port.result.Questionnaire + ip_port.result.Questionnaire_getUsecaseDetail
    // this.getUseCaseDetail(this.userId)
    console.log("SETAPI LIST**********************")
  }
}
