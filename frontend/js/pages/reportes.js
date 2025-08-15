// @ts-nocheck
async function descargarReporteVehiculos(desde, hasta){
  await http.download('/reportes/vehiculos/', { query:{ desde, hasta }, filename:`reporte_vehiculos_${desde}_${hasta}.csv` });
}
async function descargarReporteKilometraje(vehiculo_id, desde, hasta){
  await http.download('/reportes/kilometraje/', { query:{ vehiculo_id, desde, hasta }, filename:`km_${vehiculo_id}_${desde}_${hasta}.pdf` });
}
document.getElementById('btn-rv')?.addEventListener('click', ()=> descargarReporteVehiculos(document.getElementById('rv-desde').value, document.getElementById('rv-hasta').value));
document.getElementById('btn-rk')?.addEventListener('click', ()=> descargarReporteKilometraje(document.getElementById('rk-id').value, document.getElementById('rk-desde').value, document.getElementById('rk-hasta').value));
