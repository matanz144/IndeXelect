import {NgModule} from '@angular/core';
import {Routes , RouterModule} from '@angular/router';
import {NotFoundComponent} from './not-found/not-found.component';
import {SelectIndexComponent} from './select-index/select-index.component';
import {ResultsComponent} from './results/results.component';
import {ViewPlateComponent} from './view-plate/view-plate.component';


const appRouts: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'select-index'},
  { path: 'select-index', component: SelectIndexComponent },
  { path: 'results', component: ResultsComponent },
  { path: 'view-plate', component: ViewPlateComponent },
  { path: 'not-found', component: NotFoundComponent},
  { path: '**', redirectTo: '/not-found' }

];

@NgModule({
  // imports: [RouterModule.forRoot(appRouts, {useHash: true})],
  imports: [RouterModule.forRoot(appRouts, {useHash: true})],
  exports: [RouterModule]
})
export class AppRoutingModule {

}
