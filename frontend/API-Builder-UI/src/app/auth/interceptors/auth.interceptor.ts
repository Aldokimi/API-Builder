import { Injectable } from '@angular/core';
import {
    HttpRequest,
    HttpHandler,
    HttpEvent,
    HttpInterceptor,
    HTTP_INTERCEPTORS
} from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from '../services/auth.service';


@Injectable()
export class AuthInterceptor implements HttpInterceptor {

    constructor(private authService : AuthService) {}

    intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
        if(this.authService.token){
        request = request.clone({
            headers: request.headers.set('Authorization',`Bearer ${this.authService.token.substring(1,this.authService.token.length-1)!}`)
        
        })
    }
        return next.handle(request);
    }
}

export const AuthInterceptorProvider = {
    provide : HTTP_INTERCEPTORS,
    useClass: AuthInterceptor,
    multi: true,
};