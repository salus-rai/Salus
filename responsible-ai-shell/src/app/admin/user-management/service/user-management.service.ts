/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';

import { ApplicationConfigService } from '../../../core/config/application-config.service';
import { createRequestOption } from '../../../core/request/request-util';
import { Pagination } from '../../../core/request/request.model';
import { IUser, getUserIdentifier } from '../user-management.model';
import { urlList } from '../../../utils/urlList';

@Injectable({ providedIn: 'root' })
export class UserManagementService {
  private resourceUrl = urlList.server_api_url +'/users';
 

  constructor(private http: HttpClient, private applicationConfigService: ApplicationConfigService) {}

  create(user: IUser): Observable<IUser> {
    return this.http.post<IUser>(this.resourceUrl, user);
  }

  update(user: IUser): Observable<IUser> {
     return this.http.put<IUser>(urlList.server_api_url + '/users/updateUser', user)
  }

  find(id: number): Observable<IUser> {
    return this.http.get<IUser>(urlList.server_api_url + '/users/getUser?id='+id);
  }

  query(req?: Pagination): Observable<any> {
    const options = createRequestOption(req);
    return this.http.get<any>(this.resourceUrl, { params: options, responseType: 'json'  });
  }

  delete(id: number): Observable<{}> {
    return this.http.delete(urlList.server_api_url + '/users/delete?id='+id);
  }

  authorities(): Observable<string[]> {
    return this.http.get<string[]>(urlList.server_api_url + '/users/authorities');
  }
}
