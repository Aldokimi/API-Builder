import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { CookieService } from 'ngx-cookie';
import { catchError, map, Observable, of, tap } from 'rxjs';
import { User } from '../models/user';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  constructor(
    private http: HttpClient,
    private router: Router,
    private cookieService: CookieService
  ) {}
  myURL = `//127.0.0.1:8000/api/`;

  getAllUsers() {
    return this.http.get(`${this.myURL}users/`).pipe(
      tap(dt=>{
        console.log(dt);
        
      }),
      catchError((error) => {
        console.log(error);
        //this.router.navigate(['home']);

        return of(error);
      })
    );
  }

  getCookie(key: string) {
    return this.cookieService.get(key);
  }
  putCookie(key: string, value: string) {
    this.cookieService.put(key, value);
  }

  deleteCookie(key: string) {
    this.cookieService.remove(key);
  }

  
  getUser(id: number|string): Observable<any> {
   

    return this.http.get(`${this.myURL}users/${id}`).pipe(
      
      catchError((error) => {
       console.log(error);
        //this.router.navigate(['home']);
        this.router.navigate(['**'])
        return of(error);
      })
    );
  }




  editUser() {}
}
