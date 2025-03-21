/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, ReplaySubject, of } from 'rxjs';
import { shareReplay, tap, catchError } from 'rxjs/operators';

import { StateStorageService } from '../../../app/core/auth/state-storage.service';
import { ApplicationConfigService } from '../config/application-config.service';
import { Account } from '../../../app/core/auth/account.model';
import { environment } from 'src/environments/environment';
import { urlList } from 'src/app/utils/urlList';

@Injectable({ providedIn: 'root' })
export class AccountService {
  private userIdentity: Account | null = null;
  private authenticationState = new ReplaySubject<Account | null>(1);
  private accountCache$?: Observable<Account> | null;

  constructor(
    private http: HttpClient,
    private stateStorageService: StateStorageService,
    private router: Router,
    private applicationConfigService: ApplicationConfigService
  ) {}

  save(account: Account): Observable<{}> {
    return this.http.get<Account>(urlList.server_api_url+ '/api/account');
  }

  authenticate(identity: Account | null): void {
    this.userIdentity = identity;
    this.authenticationState.next(this.userIdentity);
    if (!identity) {
      this.accountCache$ = null;
    }
  }

  hasAnyAuthority(authorities: string[] | string): boolean {
    if (!this.userIdentity) {
      return false;
    }
    if (!Array.isArray(authorities)) {
      authorities = [authorities];
    }
    return this.userIdentity.authorities.some((authority: string) => authorities.includes(authority));
  }

  identity(force?: boolean): Observable<Account | null> {
    if (!this.accountCache$ || force || !this.isAuthenticated()) {
      this.accountCache$ = this.fetch().pipe(
        tap((account: Account) => {
          this.authenticate(account);

          if (account) {
            this.navigateToStoredUrl();
          }
        }),
        shareReplay()
      );
    }
    return this.accountCache$.pipe(catchError(() => of(null)));
  }

  isAuthenticated(): boolean {
    return this.userIdentity !== null;
  }

  getAuthenticationState(): Observable<Account | null> {
    return this.authenticationState.asObservable();
  }

  getImageUrl(): string {
    return this.userIdentity ? this.userIdentity.imageUrl! : '';
  }

  private fetch(): Observable<Account> {
    const JwtToken = sessionStorage.getItem('jhi-authenticationToken') || localStorage.getItem('jhi-authenticationToken');
    const token = JwtToken ? this.sanitizeInput(JwtToken) : null;
    console.log("JwtToken::", JwtToken);
    console.log("token::", token);
  
    // Validate the token format before using it
    if (token && !this.isValidToken(token)) {
      throw new Error('Invalid token');
    }
  
    const reqHeader = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': token ? 'Bearer ' + token : '',
    });
  
    return this.http.get<Account>(urlList.server_api_url + '/account', { headers: reqHeader });
  }
  
  private isValidToken(token: string): boolean {
    console.log("Token to validate:", token);  // Log the token to debug
    const jwtPattern = /^[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.[A-Za-z0-9-_.+/=]*$/;
    return jwtPattern.test(token);
  }
  private navigateToStoredUrl(): void {
    // previousState can be set in the authExpiredInterceptor and in the userRouteAccessService
    // if login is successful, go to stored previousState and clear previousState
    const previousUrl = this.stateStorageService.getUrl();
    if (previousUrl) {
      this.stateStorageService.clearUrl();
      this.router.navigateByUrl(previousUrl);
    }
  }
  getUserNames():string{
    const fName = this.userIdentity ? this.userIdentity.firstName! :'';
    const lName = this.userIdentity ? this.userIdentity.lastName! :'';
    let initials;
    if(fName && lName){
      initials = fName.toUpperCase().charAt(0) + lName.toUpperCase().charAt(0);
    }else{
      initials = fName.toUpperCase().charAt(0)
    }
   return initials; 
  }
  sanitizeInput(input: any): string {
    // Only remove potentially harmful characters, not those required for a valid JWT
    return input.replace(/[^A-Za-z0-9\-_.]/g, '');  // Allow only alphanumeric, -, _, and .
}
}
