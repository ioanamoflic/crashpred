data {
  int<lower=0> N;
  int<lower=0> M;
  int success[N, M];
  int attempts[N, M];
  int year[N, M];
}

parameters {
  real hyper_intercept_mean;
  real hyper_intercept_sd;
  real hyper_year_weight_mean;
  real hyper_year_weight_sd;
  real intercept[M];
  real year_weight[M];
}

transformed parameters {
  real theta[N, M];
  
  for(i in 1:N)
    for(j in 1:M)
    {
      theta[i, j] = (intercept[j] + year_weight[j] * (year[i, j] - 1980)/8)/100;
    }
      
}

model {
  // hyper prior
  hyper_intercept_mean ~ uniform(-300, 300); //normal(0, 500); //normal(0, 100); //normal(0, 100); 
  hyper_intercept_sd ~ uniform(0, 100); //normal(500, 100); //normal(100, 30); //normal(0, 50); 
  
  hyper_year_weight_mean ~ uniform(-40, 40); //normal(0, 100); //normal(0, 20); //normal(0, 10); 
  hyper_year_weight_sd ~ uniform(0, 20); //normal(150, 50); //normal(30, 10); //normal(10, 3);
  
  
  // priors
  for (i in 1:M){
    intercept[i] ~ normal(hyper_intercept_mean, hyper_intercept_sd);
    year_weight[i] ~ normal(hyper_year_weight_mean, hyper_year_weight_sd);
  }
  
  
  //year_weight ~ normal(0, 10); //uniform(0, 4); //normal(0.4, 0) //normal(4, 0.75); //uniform(0, 5); //normal(0,20);
  
  
  
  
  // likelihood
  for(i in 1:M)
    success[, i] ~ binomial_logit(attempts[, i], theta[, i]);
}
 
generated quantities {
  matrix[N, M] log_lik;
  
  for(i in 1:N)
    for(j in 1:M)
      log_lik[i, j] = binomial_logit_lpmf( success[i, j] | attempts[i, j], theta[i, j]);
}
