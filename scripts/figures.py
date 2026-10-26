"""Optional publication figures; generated from saved replay and CSV."""
import json,csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
root=Path(__file__).resolve().parents[1];rows=json.loads((root/'results/demo.json').read_text())['samples']
plt.rcParams.update({'figure.facecolor':'#071724','axes.facecolor':'#0b2030','axes.edgecolor':'#3d627a','text.color':'#dcedf7','axes.labelcolor':'#a1bece','xtick.color':'#8cabbf','ytick.color':'#8cabbf','font.size':10,'grid.color':'#29485c','savefig.facecolor':'#071724'})
fig=plt.figure(figsize=(13,8));ax=fig.add_subplot(121,projection='3d');x=np.linspace(-30,30,90);y=np.linspace(-10,10,25);X,Y=np.meshgrid(x,y);Z=.6*(X/30)**2;ax.plot_surface(X,Y,Z,color='#3c657b',alpha=.8,linewidth=0);level=rows[48]['truth_m'];ax.plot_surface(X,Y,np.where(Z<=level,level,np.nan),color='#35ccd7',alpha=.55);ax.set(xlabel='Transect x (m)',ylabel='Cross-road y (m)',zlabel='Local elevation (m)',title='Synthetic crossing at minute 48');ax.view_init(26,-58)
bx=fig.add_subplot(222);t=[r['minute'] for r in rows];bx.plot(t,[r['truth_m'] for r in rows],color='#4dd8dc',label='Crossing truth');bx.plot(t[10:],[r['forecast_m'] for r in rows[:-10]],color='#f6b96b',linestyle='--',label='+10 min forecast');bx.set(xlabel='Time (min)',ylabel='Dip depth (m)');bx.legend(frameon=False,fontsize=8);bx.grid(alpha=.4)
cx=fig.add_subplot(224);records=list(csv.DictReader((root/'results/predictions.csv').open()));errors=[[float(r['error_m']) for r in records if r['split']==key] for key in ['held_out','ood_intense']];cx.hist(errors,bins=40,color=['#4dd8dc','#f6b96b'],alpha=.7,label=['Held-out','Intense OOD']);cx.set(xlabel='Forecast error (m)',ylabel='Samples');cx.legend(frameon=False,fontsize=8);cx.grid(alpha=.4)
fig.suptitle('FLOOD DRONE · REPLAY / FORECAST / FAILURE DISTRIBUTION',fontsize=15,x=.5,y=.97);fig.text(.5,.02,'Synthetic data only. A projected 3D surface does not validate real water-depth measurements.',ha='center',color='#8cabbf',fontsize=10);fig.subplots_adjust(left=.04,right=.97,bottom=.11,top=.9,hspace=.5,wspace=.26);fig.savefig(root/'docs/images/research.png',dpi=160);plt.close(fig)
