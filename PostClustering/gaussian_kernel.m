function kerny = gaussian_kernel(kernx, FWHM)

if (nargin == 1)
  %kerny = 1/sqrt(2*pi) * exp(-kernx.^2/2);
  kerny = exp(-kernx.^2/2);
else
  sig = FWHM/sqrt(8*log(2));
  kerny = exp(-(finex-datap).^2/(2*sig^2));
  % not making the area under kernel = 1 here
end

