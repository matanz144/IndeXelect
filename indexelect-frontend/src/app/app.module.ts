import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { SelectIndexComponent } from './select-index/select-index.component';
import { HeaderComponent } from './header/header.component';
import { ResultsComponent } from './results/results.component';
import { ViewPlateComponent } from './view-plate/view-plate.component';
import { NotFoundComponent } from './not-found/not-found.component';
import {AppRoutingModule} from './app-routing.module';
import {AgGridModule} from 'ag-grid-angular';
import {FormsModule, NgForm} from '@angular/forms';
import { FileUploadModule } from 'ng2-file-upload/ng2-file-upload';
import { FileSelectDirective, FileUploader } from 'ng2-file-upload/ng2-file-upload';
import {HttpClientModule} from '@angular/common/http';
import {ResultService} from './Result.service';
import {PapaParseModule} from 'ngx-papaparse';



@NgModule({
  declarations: [
    AppComponent,
    SelectIndexComponent,
    HeaderComponent,
    ResultsComponent,
    ViewPlateComponent,
    NotFoundComponent
  ],
  imports: [
    FormsModule,
    BrowserModule,
    AppRoutingModule,
    AgGridModule.withComponents([]),
    FileUploadModule,
    HttpClientModule,
    PapaParseModule,

  ],
  providers: [ResultService],
  bootstrap: [AppComponent]
})
export class AppModule { }
