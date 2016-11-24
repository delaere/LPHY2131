#include "TF1.h"
#include "TH1.h"
#include "TMath.h"

//Gaussian
Double_t mygauss(Double_t * x, Double_t * par)
{
  Double_t arg = 0;
  if (par[2]<0) par[2]=-par[2];  // par[2]: sigma
  if (par[2] != 0) arg = (x[0] - par[1])/par[2];  // par[1]: mean
 
   return par[0]*TMath::Exp(-0.5*arg*arg)/
     (TMath::Sqrt(2*TMath::Pi())*par[2]); // par[0] is constant
 
}

//Breit-Wigner function
Double_t mybw(Double_t* x, Double_t* par)
{
  Double_t arg1 = 14.0/22.0; // 2 over pi
  Double_t arg2 = par[1]*par[1]*par[2]*par[2]; //Gamma=par[1]  M=par[2]
  Double_t arg3 = ((x[0]*x[0]) - (par[2]*par[2]))*((x[0]*x[0]) - (par[2]*par[2]));
  Double_t arg4 = x[0]*x[0]*x[0]*x[0]*((par[1]*par[1])/(par[2]*par[2]));
  return par[0]*arg1*arg2/(arg3 + arg4);
}

const double e = 2.71828182846;

//exponential function
Double_t myexpo(Double_t* x, Double_t* par)
{
  return par[0]*pow(e,par[1]*x[0]);
}

//constant function
Double_t myconst(Double_t* x, Double_t* par)
{
  return par[0];
}

// power law
Double_t myPowerlaw(Double_t* x, Double_t* par)
{
  return par[0]*pow(par[1],-x[0]);
}

//Voigtian function
Double_t myVoigt(Double_t* x, Double_t* par)
{
  return par[0]*TMath::Voigt(x[0]-par[1],par[2],par[3]) + exp(par[4]+par[5]*x[0]);		
}
