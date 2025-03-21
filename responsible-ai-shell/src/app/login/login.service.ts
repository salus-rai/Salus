/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { mergeMap } from 'rxjs/operators';

import { Account } from '../../app/core/auth/account.model';
import { AccountService } from '../../app/core/auth/account.service';
import { AuthServerProvider } from '../../app/core/auth/auth-jwt.service';
import { Login } from './login.model';
import { urlList } from '../utils/urlList';

@Injectable({ providedIn: 'root' })
export class LoginService {
  public authorityAPI = urlList.server_api_url + '/pageauthoritynew';
  public logOut =  urlList.server_api_url + '/logout';
  pages: any;
  constructor(public http: HttpClient,private accountService: AccountService, private authServerProvider: AuthServerProvider) {}

  public url:any
  // http://10.184.72.253:8080/api/v1/rai/admin/ConfigApi

  loginUrls(){
    // return this.url
    // this.http.get("http://10.184.72.253:8070/api/v1/rai/admin/ConfigApi").subscribe
    // ((res: any) => {
    //   // this.url = res
    //   console.log("only res",res)
    //   localStorage.setItem("res",JSON.stringify(res))
    //   // localStorage.setItem("res",res)
    //   // console.log("only res ARRYA",res.resultdev)



    // })
    console.log('hi india',this.url)
    return this.url

  }
  getConfigApiList(url:any): Observable<any> {
    return this.http.get<any>(url);
  }
  login(credentials: Login): Observable<Account | null> {
    return this.authServerProvider.login(credentials)
    .pipe(mergeMap(() => this.accountService.identity(true)));
  }

  logout(): any {
    let userName = this.getUserName();
    console.log("userName",userName)
    this.authServerProvider.logout().subscribe({
      complete: () =>
      this.accountService.authenticate(null) }
      );
    console.log("logout",this.logOut)
    this.http.get<any>(`${this.logOut}?username=${userName}`).subscribe(
      response => {
        console.log('Logout successful:', response);
        // Handle successful logout here
      },
      error => {
      }
    );
    return "Logged Out"
  }

  getUserName(){
    let userName = localStorage.getItem('userid')
    return userName
  }

  getPages(roles: string[]): Promise<string[]> {
    const promises = roles.map(role => {
      return this.http.get<any>(`${this.authorityAPI}?role=${role}`)
        .toPromise()
        .then(response => {
          // Store pages in local storage
          localStorage.setItem('pages', JSON.stringify(response.pages));
          return Object.keys(response.pages);
        })
        .catch(error => {
          return [];
        });
    });

    return Promise.all(promises)
      .then(pagesArray => {
        const combinedPages = pagesArray.reduce((accumulator, pages) => accumulator.concat(this.pages), []);
        return combinedPages;
      })
      .catch(error => {
        return [];
      });
  }
}
