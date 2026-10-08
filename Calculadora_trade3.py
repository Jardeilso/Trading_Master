import customtkinter as ctk
import pandas as pd
import os
from datetime import datetime

# Configuração visual
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Caminho para salvar o banco de dados na mesma pasta do executável
ARQUIVO_EXCEL = "historico_trades.xlsx"

class AppCalculadoraAvancada(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Gestão de Trade & Lucro Anual")
        self.geometry("450x650")
        self.resizable(False, False)
        
        # --- TÍTULO ---
        self.titulo = ctk.CTkLabel(self, text="📊 Gestão de Investimentos", font=ctk.CTkFont(size=20, weight="bold"))
        self.titulo.pack(pady=15)
        
        # --- CAMPOS DE ENTRADA (INPUTS) ---
        self.txt_ativo = ctk.CTkEntry(self, placeholder_text="Ativo (Ex: PETR4)", width=300)
        self.txt_ativo.pack(pady=6)
        
        self.txt_qtd = ctk.CTkEntry(self, placeholder_text="Quantidade (Ex: 100)", width=300)
        self.txt_qtd.pack(pady=6)
        
        self.txt_compra = ctk.CTkEntry(self, placeholder_text="Preço de Compra Unitário (R$)", width=300)
        self.txt_compra.pack(pady=6)
        
        self.txt_venda = ctk.CTkEntry(self, placeholder_text="Preço de Venda Unitário (R$)", width=300)
        self.txt_venda.pack(pady=6)
        
        # Novo campo: Mês/Ano da Operação (Vem preenchido com o mês atual automaticamente)
        mes_atual = datetime.now().strftime("%m/%Y")
        self.txt_data = ctk.CTkEntry(self, placeholder_text=f"Mês/Ano da Operação (Ex: {mes_atual})", width=300)
        self.txt_data.insert(0, mes_atual)
        self.txt_data.pack(pady=6)
        
        # --- BOTÕES ---
        self.btn_calcular = ctk.CTkButton(self, text="Calcular e Salvar Operação", command=self.processar_e_salvar, width=300, fg_color="green", hover_color="darkgreen")
        self.btn_calcular.pack(pady=12)
        
        self.btn_limpar = ctk.CTkButton(self, text="Limpar Campos", command=self.limpar_campos, width=300, fg_color="gray", hover_color="darkgray")
        self.btn_limpar.pack(pady=2)
        
        # --- PAINEL DE RESULTADOS (OUTPUTS) ---
        self.lbl_resultado_trade = ctk.CTkLabel(self, text="Aguardando operação...", font=ctk.CTkFont(size=13), justify="left")
        self.lbl_resultado_trade.pack(pady=15)
        
        # Caixa de Destaque para o Consolidado Anual/Mensal
        self.frame_painel = ctk.CTkFrame(self, width=380, height=140)
        self.frame_painel.pack(pady=10, fill="x", padx=35)
        self.frame_painel.pack_propagate(False)
        
        self.lbl_painel_titulo = ctk.CTkLabel(self.frame_painel, text="🏆 PAINEL CONSOLIDADO DA CARTEIRA", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_painel_titulo.pack(pady=5)
        
        self.lbl_metricas = ctk.CTkLabel(self.frame_painel, text="Lucro no Mês: R$ 0.00\nLucro no Ano: R$ 0.00\nRentabilidade Anual: 0.00%", font=ctk.CTkFont(size=13))
        self.lbl_metricas.pack(pady=5)
        
        # Carrega o painel com os dados históricos já existentes ao abrir o app
        self.atualizar_painel_consolidado()

    def limpar_campos(self):
        self.txt_ativo.delete(0, 'end')
        self.txt_qtd.delete(0, 'end')
        self.txt_compra.delete(0, 'end')
        self.txt_venda.delete(0, 'end')
        self.lbl_resultado_trade.configure(text="Campos limpos. Aguardando nova operação.", text_color="system")

    def processar_e_salvar(self):
        try:
            ativo = self.txt_ativo.get().strip().upper()
            qtd = int(self.txt_qtd.get())
            p_compra = float(self.txt_compra.get().replace(",", "."))
            p_venda = float(self.txt_venda.get().replace(",", "."))
            data_mes = self.txt_data.get().strip()
            
            if not ativo or qtd <= 0 or p_compra <= 0 or p_venda <= 0 or not data_mes:
                self.lbl_resultado_trade.configure(text="❌ Erro: Preencha todos os campos corretamente!", text_color="orange")
                return

            custo_total = qtd * p_compra
            venda_total = qtd * p_venda
            lucro_trade = venda_total - custo_total
            rentabilidade_trade = (lucro_trade / custo_total) * 100
            
            # --- BANCO DE DADOS (SALVAR NO EXCEL) ---
            nova_linha = {
                'Data_Mes': data_mes, 'Ativo': ativo, 'Quantidade': qtd,
                'Preco_Compra': p_compra, 'Preco_Venda': p_venda,
                'Custo_Total': custo_total, 'Venda_Total': venda_total, 'Lucro_Prejuizo': lucro_trade
            }
            
            if os.path.exists(ARQUIVO_EXCEL):
                df_historico = pd.read_excel(ARQUIVO_EXCEL)
                df_historico = pd.concat([df_historico, pd.DataFrame([nova_linha])], ignore_index=True)
            else:
                df_historico = pd.DataFrame([nova_linha])
                
            df_historico.to_excel(ARQUIVO_EXCEL, index=False)
            
            # --- EXIBIR RESULTADO DO TRADE ATUAL ---
            res_texto = f"📈 Trade {ativo}: Custo R$ {custo_total:,.2f} | Venda R$ {venda_total:,.2f}\n"
            if lucro_trade > 0:
                self.lbl_resultado_trade.configure(text=res_texto + f"🟢 LUCRO: R$ {lucro_trade:,.2f} (+{rentabilidade_trade:.2f}%)", text_color="green")
            elif lucro_trade < 0:
                self.lbl_resultado_trade.configure(text=res_texto + f"🔴 PREJUÍZO: R$ {abs(lucro_trade):,.2f} ({rentabilidade_trade:.2f}%)", text_color="red")
            else:
                self.lbl_resultado_trade.configure(text=res_texto + "🟡 EMPATE: R$ 0.00 (0.00%)", text_color="gray")
            
            # Atualiza o painel consolidado com a nova operação inclusa
            self.atualizar_painel_consolidado()
            
        except ValueError:
            self.lbl_resultado_trade.configure(text="❌ Erro: Verifique os números digitados!", text_color="orange")

    def atualizar_painel_consolidado(self):
        if not os.path.exists(ARQUIVO_EXCEL):
            return
            
        try:
            df = pd.read_excel(ARQUIVO_EXCEL)
            if df.empty:
                return
                
            # 🛡️ BLINDAGEM DE DATAS: Converte a coluna para texto estável e extrai as datas reais
            df['Data_M_Str'] = df['Data_Mes'].astype(str).str.strip()
            df['Data_Convertida'] = pd.to_datetime(df['Data_M_Str'], format='%m/%Y', errors='coerce')
            df.loc[df['Data_Convertida'].isna(), 'Data_Convertida'] = pd.to_datetime(df['Data_M_Str'], errors='coerce')
            
            mes_atual_filtro = self.txt_data.get().strip()
            
            try:
                partes = mes_atual_filtro.split("/")
                mes_alvo = int(partes[0])
                ano_alvo = int(partes[1])
            except:
                mes_alvo = datetime.now().month
                ano_alvo = datetime.now().year
            
            # Filtros matemáticos por objetos datetime estruturados
            df_mes = df[(df['Data_Convertida'].dt.month == mes_alvo) & (df['Data_Convertida'].dt.year == ano_alvo)]
            df_ano = df[df['Data_Convertida'].dt.year == ano_alvo]
            
            # Cálculos consolidados sem furos de tipos do Excel
            lucro_mes = df_mes['Lucro_Prejuizo'].sum()
            lucro_ano = df_ano['Lucro_Prejuizo'].sum()
            custo_ano = df_ano['Custo_Total'].sum()
            
            rentabilidade_anual = (lucro_ano / custo_ano) * 100 if custo_ano > 0 else 0.0
            
            # Formatação de cores no painel dependendo do resultado anual
            cor_painel = "green" if lucro_ano >= 0 else "red"
            
            texto_painel = (
                f"📅 Lucro no Mês ({mes_atual_filtro}): R$ {lucro_mes:,.2f}\n"
                f"🗓️ Lucro Acumulado no Ano ({ano_alvo}): R$ {lucro_ano:,.2f}\n"
                f"📊 Rentabilidade Anual Realizada: {rentabilidade_anual:.2f}%"
            )
            self.lbl_metricas.configure(text=texto_painel)
            self.lbl_painel_titulo.configure(text_color=cor_painel)
            
        except Exception as e:
            print(f"Erro ao ler painel: {e}")

if __name__ == "__main__":
    app = AppCalculadoraAvancada()
    app.mainloop()
