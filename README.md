# Web scraping options pricer

## Web scraping

Using web scraping algos to get market data (Ticker/K/T otpion quotes, spot, dividends, spot/options volumes, ...).</br>
Source is [Yahoo finance](yahoo.finance.com).</br></br>
Scraping tech relies on selenium, beautifulsoup and chromedriver.</br>

## Dahboarding

Interactive dashboard enables user to plot prices and vol surface (3D surface to come)</br>
A pricing interface will be added soon.</br></br>
Dashboarding is achieved via plotly's dash library.

## Quant library

Inhouse quant lib with handy data-handling</br></br>
Vol surface construction using:</br>
- Polynomial regression
- Natural cubic splines
- Smoothing cubic splines
- Blend of smoothed observations (using smoothing splines) and polynomial regression (to come soon)
</br></br>
Pricing library will house (in progress):
- Local volatility under Dupire's framework (vol or price version, too see)
- LSV model 
- Hard-coded deep learning lib, autoencoders for vol surface denoising and construction (in progress)
- Hard-coded optimizers (to come soon)
- Blending statistical model (could range anywhere from basic stuff up to deepL)
- Blended vol model (LV + (or *) adjustment (or scaling) factor to mimick LV-LSV pricing error)

## Simulated order-placing (to come)
Illustrative module faking options order-placing from the click of dash buttons</br>
Based on CBOE's FIX protocol for US options : [CBOE FIX](https://cdn.cboe.com/resources/membership/US_Options_FIX_Specification.pdf)</br>

