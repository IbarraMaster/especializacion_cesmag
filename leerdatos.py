import pandas as pd
import numpy as np

# Leer el archivo CSV
df = pd.read_csv('datos_sinteticos.csv')

print("=" * 70)
print("ANALISIS DE DATOS DE CAMPANAS PUBLICITARIAS")
print("=" * 70)

# ============ DATOS GENERALES ============
print(f"\nDATOS GENERALES:")
print(f"   Total de campanas: {len(df)}")
print(f"   Plataformas utilizadas: {df['plataforma'].nunique()} - {', '.join(df['plataforma'].unique())}")
print(f"   Tipos de campana: {df['tipo_campana'].nunique()}")

# ============ PRESUPUESTO Y REVENUE ============
print(f"\nPRESUPUESTO Y REVENUE:")
print(f"   Presupuesto diario total: ${df['presupuesto_diario'].sum():,.2f}")

print(f"   Presupuesto promedio por campana: ${df['presupuesto_diario'].mean():,.2f}")
print(f"   Revenue total generado: ${df['revenue_generado'].sum():,.2f}")
print(f"   ROAS promedio: {df['roas'].mean():.2f}x")

# ============ RENDIMIENTO POR PLATAFORMA ============
print(f"\nRENDIMIENTO POR PLATAFORMA:")
plataforma_stats = df.groupby('plataforma').agg({
    'revenue_generado': 'sum',
    'costo_total': 'sum',
    'clicks': 'sum',
    'conversiones': 'sum',
    'roas': 'mean'
}).round(2)

for plat, row in plataforma_stats.iterrows():
    print(f"\n   {plat}:")
    print(f"     - Revenue: ${row['revenue_generado']:,.2f}")
    print(f"     - Costo Total: ${row['costo_total']:,.2f}")
    print(f"     - Clicks: {int(row['clicks'])}")
    print(f"     - ROAS: {row['roas']:.2f}x")
    print(f"     - Conversiones: {int(row['conversiones'])}")

# ============ RENDIMIENTO POR TIPO DE CAMPANA ============
print(f"\n\nRENDIMIENTO POR TIPO DE CAMPANA:")
tipo_stats = df.groupby('tipo_campana').agg({
    'revenue_generado': 'mean',
    'conversion_rate': 'mean',
    'engagement_rate': 'mean',
    'roas': 'mean'
}).round(2).sort_values('roas', ascending=False)

for tipo, row in tipo_stats.iterrows():
    print(f"\n   {tipo}:")
    print(f"     - ROAS: {row['roas']:.2f}x")
    print(f"     - Conv.Rate: {row['conversion_rate']:.2f}%")
    print(f"     - Engagement: {row['engagement_rate']:.2f}%")
    print(f"     - Revenue promedio: ${row['revenue_generado']:,.2f}")

# ============ RENDIMIENTO POR AUDIENCIA ============
print(f"\n\nRENDIMIENTO POR AUDIENCIA:")
audiencia_stats = df.groupby('audiencia_objetivo').agg({
    'conversiones': 'sum',
    'ctr': 'mean',
    'conversion_rate': 'mean'
}).round(2).sort_values('conversion_rate', ascending=False)

for aud, row in audiencia_stats.iterrows():
    print(f"\n   {aud}:")
    print(f"     - Conv.Rate: {row['conversion_rate']:.2f}%")
    print(f"     - CTR: {row['ctr']:.2f}%")
    print(f"     - Total Conversiones: {int(row['conversiones'])}")

# ============ METRICAS DE EFICIENCIA ============
print(f"\n\nMETRICAS DE EFICIENCIA:")
print(f"   CTR promedio: {df['ctr'].mean():.2f}%")
print(f"   Conversion Rate promedio: {df['conversion_rate'].mean():.2f}%")
print(f"   Engagement Rate promedio: {df['engagement_rate'].mean():.2f}%")
print(f"   CPA promedio: ${df['cpa'].mean():.2f}")
print(f"   CPC promedio: ${df['cpc'].mean():.2f}")
print(f"   Tiempo promedio de conversion: {df['tiempo_conversion_hrs'].mean():.1f} horas")

# ============ TOP 3 MEJORES CAMPANAS ============
print(f"\n\nTOP 3 MEJORES CAMPANAS (por ROAS):")
top3 = df.nlargest(3, 'roas')[['campana_id', 'plataforma', 'tipo_campana', 'roas', 'revenue_generado', 'conversiones']]
for idx, (i, row) in enumerate(top3.iterrows(), 1):
    print(f"\n   {idx}. {row['campana_id']} ({row['plataforma']})")
    print(f"      - Tipo: {row['tipo_campana']}")
    print(f"      - ROAS: {row['roas']:.2f}x")
    print(f"      - Revenue: ${row['revenue_generado']:,.2f}")
    print(f"      - Conversiones: {int(row['conversiones'])}")

# ============ TOP 3 PEORES CAMPANAS ============
print(f"\n\nTOP 3 PEORES CAMPANAS (por ROAS):")
bottom3 = df.nsmallest(3, 'roas')[['campana_id', 'plataforma', 'tipo_campana', 'roas', 'revenue_generado', 'conversiones']]
for idx, (i, row) in enumerate(bottom3.iterrows(), 1):
    print(f"\n   {idx}. {row['campana_id']} ({row['plataforma']})")
    print(f"      - Tipo: {row['tipo_campana']}")
    print(f"      - ROAS: {row['roas']:.2f}x")
    print(f"      - Revenue: ${row['revenue_generado']:,.2f}")
    print(f"      - Conversiones: {int(row['conversiones'])}")

# ============ ANALISIS ADICIONAL ============
print(f"\n\nANALISIS ADICIONAL:")
print(f"   Plataforma mas rentable: {df.loc[df['revenue_generado'].idxmax(), 'plataforma']} (${df['revenue_generado'].max():,.2f})")
print(f"   Plataforma mas eficiente: {df.loc[df['roas'].idxmax(), 'plataforma']} ({df['roas'].max():.2f}x ROAS)")
print(f"   Audiencia mas convertidora: Edad {df.loc[df['conversion_rate'].idxmax(), 'audiencia_objetivo']} ({df['conversion_rate'].max():.2f}% conversion)")
print(f"   Mejor tipo de campana: {df.loc[df['revenue_generado'].idxmax(), 'tipo_campana']}")

print("\n" + "=" * 70)

# ============ GRAFICOS ============
import matplotlib.pyplot as plt
import seaborn as sns

# Configurar estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 12)
plt.rcParams['font.size'] = 10

# Crear figura con subplots
fig = plt.figure(figsize=(18, 14))

# 1. REVENUE POR PLATAFORMA
ax1 = plt.subplot(3, 3, 1)
plat_revenue = df.groupby('plataforma')['revenue_generado'].sum().sort_values(ascending=False)
colors_plat = ['#2ecc71', '#e74c3c', '#3498db', '#f39c12']
plat_revenue.plot(kind='bar', ax=ax1, color=colors_plat)
ax1.set_title('Revenue Total por Plataforma', fontweight='bold', fontsize=12)
ax1.set_ylabel('Revenue ($)')
ax1.set_xlabel('')
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
for i, v in enumerate(plat_revenue):
    ax1.text(i, v + 200, f'${v:,.0f}', ha='center', fontweight='bold')

# 2. ROAS POR PLATAFORMA
ax2 = plt.subplot(3, 3, 2)
plat_roas = df.groupby('plataforma')['roas'].mean().sort_values(ascending=False)
plat_roas.plot(kind='bar', ax=ax2, color=colors_plat)
ax2.set_title('ROAS Promedio por Plataforma', fontweight='bold', fontsize=12)
ax2.set_ylabel('ROAS (x)')
ax2.set_xlabel('')
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
ax2.axhline(y=df['roas'].mean(), color='r', linestyle='--', label='ROAS Promedio Global')
ax2.legend()
for i, v in enumerate(plat_roas):
    ax2.text(i, v + 0.15, f'{v:.2f}x', ha='center', fontweight='bold')

# 3. CONVERSIONES POR PLATAFORMA
ax3 = plt.subplot(3, 3, 3)
plat_conv = df.groupby('plataforma')['conversiones'].sum().sort_values(ascending=False)
plat_conv.plot(kind='bar', ax=ax3, color=colors_plat)
ax3.set_title('Total de Conversiones por Plataforma', fontweight='bold', fontsize=12)
ax3.set_ylabel('Conversiones')
ax3.set_xlabel('')
plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha='right')
for i, v in enumerate(plat_conv):
    ax3.text(i, v + 10, f'{int(v)}', ha='center', fontweight='bold')

# 4. REVENUE POR TIPO DE CAMPANA
ax4 = plt.subplot(3, 3, 4)
tipo_revenue = df.groupby('tipo_campana')['revenue_generado'].mean().sort_values(ascending=False)
colors_tipo = plt.cm.Set3(range(len(tipo_revenue)))
tipo_revenue.plot(kind='bar', ax=ax4, color=colors_tipo)
ax4.set_title('Revenue Promedio por Tipo de Campaña', fontweight='bold', fontsize=12)
ax4.set_ylabel('Revenue Promedio ($)')
ax4.set_xlabel('')
plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45, ha='right')
for i, v in enumerate(tipo_revenue):
    ax4.text(i, v + 100, f'${v:,.0f}', ha='center', fontweight='bold')

# 5. CONVERSION RATE POR TIPO DE CAMPANA
ax5 = plt.subplot(3, 3, 5)
tipo_conv_rate = df.groupby('tipo_campana')['conversion_rate'].mean().sort_values(ascending=False)
tipo_conv_rate.plot(kind='bar', ax=ax5, color=colors_tipo)
ax5.set_title('Conversion Rate Promedio por Tipo', fontweight='bold', fontsize=12)
ax5.set_ylabel('Conversion Rate (%)')
ax5.set_xlabel('')
plt.setp(ax5.xaxis.get_majorticklabels(), rotation=45, ha='right')
for i, v in enumerate(tipo_conv_rate):
    ax5.text(i, v + 0.2, f'{v:.2f}%', ha='center', fontweight='bold')

# 6. ENGAGEMENT RATE POR TIPO DE CAMPANA
ax6 = plt.subplot(3, 3, 6)
tipo_engagement = df.groupby('tipo_campana')['engagement_rate'].mean().sort_values(ascending=False)
tipo_engagement.plot(kind='bar', ax=ax6, color=colors_tipo)
ax6.set_title('Engagement Rate Promedio por Tipo', fontweight='bold', fontsize=12)
ax6.set_ylabel('Engagement Rate (%)')
ax6.set_xlabel('')
plt.setp(ax6.xaxis.get_majorticklabels(), rotation=45, ha='right')
for i, v in enumerate(tipo_engagement):
    ax6.text(i, v + 0.2, f'{v:.2f}%', ha='center', fontweight='bold')

# 7. CONVERSION RATE POR AUDIENCIA
ax7 = plt.subplot(3, 3, 7)
aud_order = df.groupby('audiencia_objetivo')['conversion_rate'].mean().sort_values(ascending=False).index
aud_conv_rate = df.groupby('audiencia_objetivo')['conversion_rate'].mean().reindex(aud_order)
colors_aud = plt.cm.Spectral(np.linspace(0, 1, len(aud_conv_rate)))
aud_conv_rate.plot(kind='bar', ax=ax7, color=colors_aud)
ax7.set_title('Conversion Rate por Grupo de Edad', fontweight='bold', fontsize=12)
ax7.set_ylabel('Conversion Rate (%)')
ax7.set_xlabel('Grupo de Edad')
plt.setp(ax7.xaxis.get_majorticklabels(), rotation=45, ha='right')
for i, v in enumerate(aud_conv_rate):
    ax7.text(i, v + 0.3, f'{v:.2f}%', ha='center', fontweight='bold')

# 8. CONVERSIONES TOTALES POR AUDIENCIA
ax8 = plt.subplot(3, 3, 8)
aud_conversiones = df.groupby('audiencia_objetivo')['conversiones'].sum().reindex(aud_order[::-1])
aud_conversiones.plot(kind='barh', ax=ax8, color=colors_aud[::-1])
ax8.set_title('Total de Conversiones por Grupo de Edad', fontweight='bold', fontsize=12)
ax8.set_xlabel('Conversiones')
for i, v in enumerate(aud_conversiones):
    ax8.text(v + 5, i, f'{int(v)}', va='center', fontweight='bold')

# 9. CTR vs CONVERSION RATE (Scatter)
ax9 = plt.subplot(3, 3, 9)
scatter = ax9.scatter(df['ctr'], df['conversion_rate'], s=df['revenue_generado']*2, 
                      c=df['roas'], cmap='RdYlGn', alpha=0.6, edgecolors='black', linewidth=1)
ax9.set_title('CTR vs Conversion Rate\n(tamaño=revenue, color=ROAS)', fontweight='bold', fontsize=12)
ax9.set_xlabel('CTR (%)')
ax9.set_ylabel('Conversion Rate (%)')
plt.colorbar(scatter, ax=ax9, label='ROAS')

plt.tight_layout()
plt.savefig('analisis_campanas.png', dpi=300, bbox_inches='tight')
print("\n✓ Grafico guardado como 'analisis_campanas.png'")
plt.show()

# ============ GRAFICOS ADICIONALES ============
fig2, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Presupuesto vs Revenue por Campaña
ax = axes[0, 0]
top_campanas = df.nlargest(10, 'revenue_generado')
x = range(len(top_campanas))
width = 0.35
ax.bar([i - width/2 for i in x], top_campanas['presupuesto_diario'], width, label='Presupuesto', color='#3498db')
ax.bar([i + width/2 for i in x], top_campanas['revenue_generado'], width, label='Revenue', color='#2ecc71')
ax.set_title('Top 10 Campañas: Presupuesto vs Revenue', fontweight='bold', fontsize=12)
ax.set_ylabel('Monto ($)')
ax.set_xlabel('Campaña')
ax.set_xticks(x)
ax.set_xticklabels(top_campanas['campana_id'], rotation=45, ha='right')
ax.legend()
ax.grid(True, alpha=0.3)

# 2. ROAS por Campaña
ax = axes[0, 1]
roas_sorted = df.nlargest(10, 'roas')[['campana_id', 'roas']].sort_values('roas')
colors_roas = ['#e74c3c' if x < df['roas'].mean() else '#2ecc71' for x in roas_sorted['roas']]
roas_sorted.set_index('campana_id')['roas'].plot(kind='barh', ax=ax, color=colors_roas)
ax.set_title('Top 10 Campañas por ROAS', fontweight='bold', fontsize=12)
ax.set_xlabel('ROAS (x)')
ax.axvline(x=df['roas'].mean(), color='r', linestyle='--', linewidth=2, label='ROAS Promedio')
ax.legend()
for i, v in enumerate(roas_sorted['roas']):
    ax.text(v + 0.2, i, f'{v:.2f}x', va='center', fontweight='bold')

# 3. Distribución de métricas clave
ax = axes[1, 0]
metrics = ['ctr', 'conversion_rate', 'engagement_rate']
data_metrics = [df['ctr'], df['conversion_rate'], df['engagement_rate']]
bp = ax.boxplot(data_metrics, labels=['CTR (%)', 'Conv.Rate (%)', 'Engagement (%)'], patch_artist=True)
for patch, color in zip(bp['boxes'], ['#3498db', '#2ecc71', '#f39c12']):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
ax.set_title('Distribución de Métricas Clave', fontweight='bold', fontsize=12)
ax.set_ylabel('Valor (%)')
ax.grid(True, alpha=0.3, axis='y')

# 4. CPA vs CPC por Plataforma
ax = axes[1, 1]
plat_cpa = df.groupby('plataforma')['cpa'].mean()
plat_cpc = df.groupby('plataforma')['cpc'].mean()
x = range(len(plat_cpa))
width = 0.35
ax.bar([i - width/2 for i in x], plat_cpc, width, label='CPC ($)', color='#3498db')
ax.bar([i + width/2 for i in x], plat_cpa, width, label='CPA ($)', color='#e74c3c')
ax.set_title('CPC vs CPA por Plataforma', fontweight='bold', fontsize=12)
ax.set_ylabel('Costo ($)')
ax.set_xlabel('Plataforma')
ax.set_xticks(x)
ax.set_xticklabels(plat_cpa.index, rotation=45, ha='right')
ax.legend()
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('analisis_campanas_detallado.png', dpi=300, bbox_inches='tight')
print("✓ Grafico detallado guardado como 'analisis_campanas_detallado.png'")
plt.show()

print("\n¡Gráficos generados exitosamente!")
