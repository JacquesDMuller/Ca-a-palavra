import sys
import random
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout, 
                            QLabel, QPushButton, QVBoxLayout, QHBoxLayout, 
                            QComboBox, QMessageBox, QFrame, QFileDialog,
                            QInputDialog, QListWidget, QDialog, QLineEdit)
from PyQt5.QtGui import QFont, QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QPoint, QTimer

# Lista de palavras em português para diferentes níveis
PALAVRAS_PADRAO = {
    'Fácil': ['CASA', 'BOLA', 'GATO', 'MESA', 'LIVRO', 'CARRO', 'PORTA', 'FLOR', 'PEIXE', 'ÁGUA'],
    'Médio': ['BANANA', 'ESCOLA', 'JANELA', 'CADEIRA', 'TELEFONE', 'CANETA', 'SAPATO', 'CAMISA', 'JARDIM', 'COZINHA'],
    'Difícil': ['BORBOLETA', 'COMPUTADOR', 'CHOCOLATE', 'BIBLIOTECA', 'RESTAURANTE', 'BICICLETA', 'PROFESSOR', 'MONTANHA', 'ELEFANTE', 'TRAVESSEIRO']
}

# Direções possíveis para as palavras
DIRECOES = [
    (0, 1),   # Horizontal (direita)
    (1, 0),   # Vertical (baixo)
    (1, 1),   # Diagonal (baixo-direita)
    (1, -1),  # Diagonal (baixo-esquerda)
    (0, -1),  # Horizontal (esquerda)
    (-1, 0),  # Vertical (cima)
    (-1, 1),  # Diagonal (cima-direita)
    (-1, -1)  # Diagonal (cima-esquerda)
]

class DialogoAdicionarPalavras(QDialog):
    def __init__(self, palavras_atuais, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gerenciar Palavras")
        self.setMinimumSize(400, 500)
        
        # Palavras atuais
        self.palavras = palavras_atuais.copy()
        
        # Layout principal
        layout = QVBoxLayout(self)
        
        # Lista de palavras
        label_lista = QLabel("Palavras Atuais:")
        label_lista.setFont(QFont('Arial', 12, QFont.Bold))
        layout.addWidget(label_lista)
        
        self.lista_palavras = QListWidget()
        self.lista_palavras.setFont(QFont('Arial', 12))
        self.atualizar_lista()
        layout.addWidget(self.lista_palavras)
        
        # Campo para adicionar palavra
        layout_adicionar = QHBoxLayout()
        self.campo_palavra = QLineEdit()
        self.campo_palavra.setPlaceholderText("Digite uma palavra")
        self.campo_palavra.setFont(QFont('Arial', 12))
        
        btn_adicionar = QPushButton("Adicionar")
        btn_adicionar.setFont(QFont('Arial', 12))
        btn_adicionar.clicked.connect(self.adicionar_palavra)
        
        layout_adicionar.addWidget(self.campo_palavra)
        layout_adicionar.addWidget(btn_adicionar)
        layout.addLayout(layout_adicionar)
        
        # Botão para remover palavra selecionada
        btn_remover = QPushButton("Remover Selecionada")
        btn_remover.setFont(QFont('Arial', 12))
        btn_remover.clicked.connect(self.remover_palavra)
        layout.addWidget(btn_remover)
        
        # Botões para importar/exportar
        layout_importar_exportar = QHBoxLayout()
        
        btn_importar = QPushButton("Importar de Arquivo")
        btn_importar.setFont(QFont('Arial', 12))
        btn_importar.clicked.connect(self.importar_palavras)
        
        btn_exportar = QPushButton("Exportar para Arquivo")
        btn_exportar.setFont(QFont('Arial', 12))
        btn_exportar.clicked.connect(self.exportar_palavras)
        
        layout_importar_exportar.addWidget(btn_importar)
        layout_importar_exportar.addWidget(btn_exportar)
        layout.addLayout(layout_importar_exportar)
        
        # Botões OK/Cancelar
        layout_botoes = QHBoxLayout()
        
        btn_ok = QPushButton("OK")
        btn_ok.setFont(QFont('Arial', 12))
        btn_ok.clicked.connect(self.accept)
        
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setFont(QFont('Arial', 12))
        btn_cancelar.clicked.connect(self.reject)
        
        layout_botoes.addWidget(btn_ok)
        layout_botoes.addWidget(btn_cancelar)
        layout.addLayout(layout_botoes)
    
    def atualizar_lista(self):
        self.lista_palavras.clear()
        for palavra in self.palavras:
            self.lista_palavras.addItem(palavra)
    
    def adicionar_palavra(self):
        palavra = self.campo_palavra.text().strip().upper()
        if palavra and palavra not in self.palavras:
            self.palavras.append(palavra)
            self.atualizar_lista()
            self.campo_palavra.clear()
    
    def remover_palavra(self):
        item_selecionado = self.lista_palavras.currentItem()
        if item_selecionado:
            palavra = item_selecionado.text()
            self.palavras.remove(palavra)
            self.atualizar_lista()
    
    def importar_palavras(self):
        arquivo, _ = QFileDialog.getOpenFileName(self, "Importar Palavras", "", "Arquivos de Texto (*.txt)")
        if arquivo:
            try:
                with open(arquivo, 'r', encoding='utf-8') as f:
                    for linha in f:
                        palavra = linha.strip().upper()
                        if palavra and palavra not in self.palavras:
                            self.palavras.append(palavra)
                self.atualizar_lista()
                QMessageBox.information(self, "Sucesso", "Palavras importadas com sucesso!")
            except Exception as e:
                QMessageBox.warning(self, "Erro", f"Erro ao importar palavras: {str(e)}")
    
    def exportar_palavras(self):
        arquivo, _ = QFileDialog.getSaveFileName(self, "Exportar Palavras", "", "Arquivos de Texto (*.txt)")
        if arquivo:
            try:
                with open(arquivo, 'w', encoding='utf-8') as f:
                    for palavra in self.palavras:
                        f.write(palavra + '\n')
                QMessageBox.information(self, "Sucesso", "Palavras exportadas com sucesso!")
            except Exception as e:
                QMessageBox.warning(self, "Erro", f"Erro ao exportar palavras: {str(e)}")
    
    def obter_palavras(self):
        return self.palavras

class LetraCelula(QLabel):
    def __init__(self, letra, linha, coluna):
        super().__init__(letra)
        self.letra = letra
        self.linha = linha
        self.coluna = coluna
        self.selecionado = False
        self.parte_palavra_encontrada = False
        
        # Estilo da célula
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(40, 40)
        self.setFont(QFont('Arial', 14, QFont.Bold))
        self.atualizar_estilo()
            
    def atualizar_estilo(self):
        if self.parte_palavra_encontrada:
            self.setStyleSheet("background-color: #8aff8a; color: #006400; border-radius: 5px; margin: 2px;")
        elif self.selecionado:
            self.setStyleSheet("background-color: #add8e6; color: #000080; border-radius: 5px; margin: 2px;")
        else:
            self.setStyleSheet("background-color: #f0f0f0; color: #000000; border-radius: 5px; margin: 2px;")

class LinhaSelecao(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.inicio = None
        self.fim = None
        self.setFixedSize(parent.size())
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        
    def definir_pontos(self, inicio, fim):
        self.inicio = inicio
        self.fim = fim
        self.update()
        
    def limpar(self):
        self.inicio = None
        self.fim = None
        self.update()
        
    def paintEvent(self, event):
        if self.inicio and self.fim:
            painter = QPainter(self)
            pen = QPen(QColor(0, 100, 200, 180), 5, Qt.SolidLine, Qt.RoundCap)
            painter.setPen(pen)
            painter.drawLine(self.inicio, self.fim)

class CacaPalavras(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Caça-Palavras")
        self.setMinimumSize(800, 600)
        
        # Configurações do jogo
        self.tamanho_grade = 10
        self.nivel_atual = 'Fácil'
        self.palavras_para_encontrar = []
        self.palavras_encontradas = []
        self.grade = []
        self.celulas = []
        
        # Palavras personalizadas
        self.palavras_personalizadas = {}
        self.usando_palavras_personalizadas = False
        
        # Estado da seleção
        self.selecao_ativa = False
        self.celula_inicial = None
        self.celulas_selecionadas = []
        
        # Variáveis para controle do mouse
        self.mouse_pressionado = False
        self.ultima_celula = None
        
        # Configurar a interface
        self.configurar_ui()
        
        # Iniciar novo jogo
        self.novo_jogo()
    
    def configurar_ui(self):
        # Widget central
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        
        # Layout principal
        layout_principal = QHBoxLayout(widget_central)
        
        # Painel esquerdo (grade de letras)
        painel_grade = QWidget()
        layout_grade_container = QVBoxLayout(painel_grade)
        
        # Título do jogo
        titulo = QLabel("CAÇA-PALAVRAS")
        titulo.setFont(QFont('Arial', 20, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout_grade_container.addWidget(titulo)
        
        # Container para a grade
        self.container_grade = QFrame()
        self.container_grade.setFrameShape(QFrame.StyledPanel)
        self.container_grade.setStyleSheet("background-color: white; border-radius: 10px;")
        self.layout_grade = QGridLayout(self.container_grade)
        self.layout_grade.setSpacing(0)
        
        # Linha de seleção
        self.linha_selecao = LinhaSelecao(self.container_grade)
        
        layout_grade_container.addWidget(self.container_grade)
        
        # Painel direito (controles e lista de palavras)
        painel_direito = QWidget()
        painel_direito.setMaximumWidth(250)
        layout_direito = QVBoxLayout(painel_direito)
        
        # Seletor de nível
        layout_nivel = QHBoxLayout()
        label_nivel = QLabel("Nível:")
        label_nivel.setFont(QFont('Arial', 12))
        self.combo_nivel = QComboBox()
        self.combo_nivel.addItems(['Fácil', 'Médio', 'Difícil'])
        self.combo_nivel.setFont(QFont('Arial', 12))
        self.combo_nivel.setStyleSheet("padding: 5px;")
        self.combo_nivel.currentTextChanged.connect(self.mudar_nivel)
        layout_nivel.addWidget(label_nivel)
        layout_nivel.addWidget(self.combo_nivel)
        layout_direito.addLayout(layout_nivel)
        
        # Botão para gerenciar palavras personalizadas
        self.btn_gerenciar_palavras = QPushButton("Gerenciar Palavras")
        self.btn_gerenciar_palavras.setFont(QFont('Arial', 12))
        self.btn_gerenciar_palavras.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        self.btn_gerenciar_palavras.clicked.connect(self.gerenciar_palavras)
        layout_direito.addWidget(self.btn_gerenciar_palavras)
        
        # Checkbox para usar palavras personalizadas
        layout_usar_personalizadas = QHBoxLayout()
        self.btn_usar_personalizadas = QPushButton("Usar Palavras Padrão")
        self.btn_usar_personalizadas.setFont(QFont('Arial', 12))
        self.btn_usar_personalizadas.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.btn_usar_personalizadas.clicked.connect(self.alternar_palavras_personalizadas)
        layout_direito.addWidget(self.btn_usar_personalizadas)
        
        # Botão Novo Jogo
        self.btn_novo_jogo = QPushButton("Novo Jogo")
        self.btn_novo_jogo.setFont(QFont('Arial', 12, QFont.Bold))
        self.btn_novo_jogo.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.btn_novo_jogo.clicked.connect(self.novo_jogo)
        layout_direito.addWidget(self.btn_novo_jogo)
        
        # Separador
        separador = QFrame()
        separador.setFrameShape(QFrame.HLine)
        separador.setFrameShadow(QFrame.Sunken)
        layout_direito.addWidget(separador)
        
        # Lista de palavras para encontrar
        label_palavras = QLabel("Palavras para encontrar:")
        label_palavras.setFont(QFont('Arial', 12, QFont.Bold))
        layout_direito.addWidget(label_palavras)
        
        self.layout_lista_palavras = QVBoxLayout()
        container_palavras = QWidget()
        container_palavras.setLayout(self.layout_lista_palavras)
        layout_direito.addWidget(container_palavras)
        
        # Adicionar espaço flexível
        layout_direito.addStretch()
        
        # Adicionar painéis ao layout principal
        layout_principal.addWidget(painel_grade, 3)
        layout_principal.addWidget(painel_direito, 1)
        
    def criar_grade(self):
        # Limpar grade anterior
        for i in reversed(range(self.layout_grade.count())): 
            self.layout_grade.itemAt(i).widget().setParent(None)
        
        self.celulas = []
        
        # Criar nova grade
        for i in range(self.tamanho_grade):
            linha_celulas = []
            for j in range(self.tamanho_grade):
                celula = LetraCelula(self.grade[i][j], i, j)
                self.layout_grade.addWidget(celula, i, j)
                linha_celulas.append(celula)
            self.celulas.append(linha_celulas)
    
    def atualizar_lista_palavras(self):
        # Limpar lista anterior
        for i in reversed(range(self.layout_lista_palavras.count())): 
            self.layout_lista_palavras.itemAt(i).widget().setParent(None)
        
        # Adicionar palavras à lista
        for palavra in self.palavras_para_encontrar:
            label = QLabel(palavra)
            label.setFont(QFont('Arial', 12))
            
            # Marcar palavras encontradas
            if palavra in self.palavras_encontradas:
                label.setStyleSheet("text-decoration: line-through; color: green;")
            
            self.layout_lista_palavras.addWidget(label)
    
    def gerar_grade_vazia(self):
        return [[' ' for _ in range(self.tamanho_grade)] for _ in range(self.tamanho_grade)]
    
    def pode_colocar_palavra(self, grade, palavra, linha, coluna, direcao):
        dl, dc = direcao
        for i, letra in enumerate(palavra):
            l, c = linha + i * dl, coluna + i * dc
            if not (0 <= l < self.tamanho_grade and 0 <= c < self.tamanho_grade):
                return False
            if grade[l][c] != ' ' and grade[l][c] != letra:
                return False
        return True
    
    def colocar_palavra(self, grade, palavra, linha, coluna, direcao):
        dl, dc = direcao
        for i, letra in enumerate(palavra):
            l, c = linha + i * dl, coluna + i * dc
            grade[l][c] = letra
    
    def gerar_grade(self):
        # Selecionar palavras aleatórias para o nível atual
        if self.usando_palavras_personalizadas and self.nivel_atual in self.palavras_personalizadas:
            palavras_disponiveis = self.palavras_personalizadas[self.nivel_atual].copy()
        else:
            palavras_disponiveis = PALAVRAS_PADRAO[self.nivel_atual].copy()
        
        # Verificar se há palavras disponíveis
        if not palavras_disponiveis:
            QMessageBox.warning(self, "Aviso", "Não há palavras disponíveis para este nível. Usando palavras padrão.")
            palavras_disponiveis = PALAVRAS_PADRAO[self.nivel_atual].copy()
        
        random.shuffle(palavras_disponiveis)
        
        # Determinar quantas palavras usar com base no nível
        num_palavras = min(5 if self.nivel_atual == 'Fácil' else (7 if self.nivel_atual == 'Médio' else 10), len(palavras_disponiveis))
        self.palavras_para_encontrar = palavras_disponiveis[:num_palavras]
        self.palavras_encontradas = []
        
        # Criar grade vazia
        grade = self.gerar_grade_vazia()
        
        # Colocar cada palavra na grade
        for palavra in self.palavras_para_encontrar:
            colocada = False
            tentativas = 0
            
            while not colocada and tentativas < 100:
                # Escolher posição e direção aleatórias
                direcao = random.choice(DIRECOES)
                linha = random.randint(0, self.tamanho_grade - 1)
                coluna = random.randint(0, self.tamanho_grade - 1)
                
                if self.pode_colocar_palavra(grade, palavra, linha, coluna, direcao):
                    self.colocar_palavra(grade, palavra, linha, coluna, direcao)
                    colocada = True
                
                tentativas += 1
        
        # Preencher espaços vazios com letras aleatórias
        letras = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for i in range(self.tamanho_grade):
            for j in range(self.tamanho_grade):
                if grade[i][j] == ' ':
                    grade[i][j] = random.choice(letras)
        
        return grade
    
    def novo_jogo(self):
        # Ajustar tamanho da grade com base no nível
        if self.nivel_atual == 'Fácil':
            self.tamanho_grade = 10
        elif self.nivel_atual == 'Médio':
            self.tamanho_grade = 12
        else:  # Difícil
            self.tamanho_grade = 15
        
        # Gerar nova grade
        self.grade = self.gerar_grade()
        self.criar_grade()
        self.atualizar_lista_palavras()
        
        # Limpar seleção
        self.limpar_selecao()
    
    def mudar_nivel(self, nivel):
        self.nivel_atual = nivel
        self.novo_jogo()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_pressionado = True
            
            # Verificar se o clique foi em alguma célula
            pos_local = self.container_grade.mapFrom(self, event.pos())
            
            for i, linha in enumerate(self.celulas):
                for j, celula in enumerate(linha):
                    rect = celula.geometry()
                    
                    if rect.contains(pos_local):
                        self.ultima_celula = (i, j)
                        self.celula_clicada(i, j)
                        return
        
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        if self.mouse_pressionado and self.selecao_ativa:
            pos_local = self.container_grade.mapFrom(self, event.pos())
            
            for i, linha in enumerate(self.celulas):
                for j, celula in enumerate(linha):
                    rect = celula.geometry()
                    
                    if rect.contains(pos_local) and (i, j) != self.ultima_celula:
                        self.ultima_celula = (i, j)
                        self.celula_arrastada(i, j)
                        break
        
        super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_pressionado = False
            
            if self.selecao_ativa:
                self.selecao_ativa = False
                
                # Manter células marcadas se formarem uma palavra encontrada
                palavra = ''.join(self.grade[l][c] for l, c in self.celulas_selecionadas)
                palavra_reversa = palavra[::-1]
                
                if (palavra not in self.palavras_para_encontrar or palavra in self.palavras_encontradas) and \
                   (palavra_reversa not in self.palavras_para_encontrar or palavra_reversa in self.palavras_encontradas):
                    self.limpar_selecao()
        
        super().mouseReleaseEvent(event)
    
    def celula_clicada(self, linha, coluna):
        # Iniciar nova seleção
        self.limpar_selecao()
        self.selecao_ativa = True
        self.celula_inicial = (linha, coluna)
        
        # Marcar célula como selecionada
        self.celulas[linha][coluna].selecionado = True
        self.celulas[linha][coluna].atualizar_estilo()
        self.celulas_selecionadas = [(linha, coluna)]
    
    def celula_arrastada(self, linha, coluna):
        # Se não houver seleção ativa ou a célula já estiver selecionada, ignorar
        if not self.selecao_ativa or (linha, coluna) in self.celulas_selecionadas:
            return
        
        # Verificar se a célula está na mesma linha, coluna ou diagonal da célula inicial
        linha_inicial, coluna_inicial = self.celula_inicial
        
        # Calcular a direção da seleção
        dl = 0 if linha == linha_inicial else (1 if linha > linha_inicial else -1)
        dc = 0 if coluna == coluna_inicial else (1 if coluna > coluna_inicial else -1)
        
        # Se não for uma direção válida, ignorar
        if dl == 0 and dc == 0:
            return
        
        # Limpar seleção anterior
        for l, c in self.celulas_selecionadas:
            if not self.celulas[l][c].parte_palavra_encontrada:
                self.celulas[l][c].selecionado = False
                self.celulas[l][c].atualizar_estilo()
        
        # Criar nova seleção na direção determinada
        self.celulas_selecionadas = []
        
        # Calcular distância
        if dl != 0 and dc != 0:  # Diagonal
            distancia = min(
                abs(linha - linha_inicial) if dl != 0 else float('inf'),
                abs(coluna - coluna_inicial) if dc != 0 else float('inf')
            )
        else:  # Horizontal ou vertical
            distancia = max(abs(linha - linha_inicial), abs(coluna - coluna_inicial))
        
        # Selecionar células na linha
        for i in range(distancia + 1):
            l = linha_inicial + i * dl
            c = coluna_inicial + i * dc
            
            if 0 <= l < self.tamanho_grade and 0 <= c < self.tamanho_grade:
                self.celulas[l][c].selecionado = True
                self.celulas[l][c].atualizar_estilo()
                self.celulas_selecionadas.append((l, c))
        
        # Atualizar linha de seleção visual
        if self.celulas_selecionadas:
            # Obter coordenadas do centro das células
            inicio_l, inicio_c = self.celulas_selecionadas[0]
            fim_l, fim_c = self.celulas_selecionadas[-1]
            
            inicio_widget = self.celulas[inicio_l][inicio_c]
            fim_widget = self.celulas[fim_l][fim_c]
            
            inicio_pos = inicio_widget.mapTo(inicio_widget.parent(), QPoint(inicio_widget.width() // 2, inicio_widget.height() // 2))
            fim_pos = fim_widget.mapTo(fim_widget.parent(), QPoint(fim_widget.width() // 2, fim_widget.height() // 2))
            
            self.linha_selecao.definir_pontos(inicio_pos, fim_pos)
        
        # Verificar se formou uma palavra
        self.verificar_palavra_selecionada()
    
    def verificar_palavra_selecionada(self):
        # Obter a palavra formada pela seleção atual
        palavra = ''.join(self.grade[l][c] for l, c in self.celulas_selecionadas)
        palavra_reversa = palavra[::-1]
        
        # Verificar se a palavra está na lista
        if palavra in self.palavras_para_encontrar and palavra not in self.palavras_encontradas:
            self.palavras_encontradas.append(palavra)
            self.marcar_palavra_encontrada()
            self.atualizar_lista_palavras()
            self.verificar_vitoria()
        elif palavra_reversa in self.palavras_para_encontrar and palavra_reversa not in self.palavras_encontradas:
            self.palavras_encontradas.append(palavra_reversa)
            self.marcar_palavra_encontrada()
            self.atualizar_lista_palavras()
            self.verificar_vitoria()
    
    def marcar_palavra_encontrada(self):
        for l, c in self.celulas_selecionadas:
            self.celulas[l][c].parte_palavra_encontrada = True
            self.celulas[l][c].selecionado = False
            self.celulas[l][c].atualizar_estilo()
    
    def limpar_selecao(self):
        self.selecao_ativa = False
        self.celula_inicial = None
        
        for linha in self.celulas:
            for celula in linha:
                if not celula.parte_palavra_encontrada:
                    celula.selecionado = False
                    celula.atualizar_estilo()
        
        self.celulas_selecionadas = []
        self.linha_selecao.limpar()
    
    def verificar_vitoria(self):
        if len(self.palavras_encontradas) == len(self.palavras_para_encontrar):
            QMessageBox.information(self, "Parabéns!", 
                                   f"Você encontrou todas as {len(self.palavras_para_encontrar)} palavras!")
            self.novo_jogo()
    
    def gerenciar_palavras(self):
        # Obter palavras do nível atual
        nivel = self.nivel_atual
        if nivel not in self.palavras_personalizadas:
            # Se não houver palavras personalizadas para este nível, usar as padrão
            self.palavras_personalizadas[nivel] = PALAVRAS_PADRAO[nivel].copy()
        
        # Abrir diálogo para gerenciar palavras
        dialogo = DialogoAdicionarPalavras(self.palavras_personalizadas[nivel], self)
        if dialogo.exec_() == QDialog.Accepted:
            # Atualizar palavras personalizadas
            self.palavras_personalizadas[nivel] = dialogo.obter_palavras()
            
            # Se estiver usando palavras personalizadas, atualizar o jogo
            if self.usando_palavras_personalizadas:
                self.novo_jogo()
    
    def alternar_palavras_personalizadas(self):
        self.usando_palavras_personalizadas = not self.usando_palavras_personalizadas
        
        if self.usando_palavras_personalizadas:
            self.btn_usar_personalizadas.setText("Usar Palavras Padrão")
            self.btn_usar_personalizadas.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                    border-radius: 5px;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                }
            """)
        else:
            self.btn_usar_personalizadas.setText("Usar Palavras Personalizadas")
            self.btn_usar_personalizadas.setStyleSheet("""
                QPushButton {
                    background-color: #27ae60;
                    color: white;
                    border-radius: 5px;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #2ecc71;
                }
            """)
        
        # Reiniciar o jogo com as novas palavras
        self.novo_jogo()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Definir estilo global
    app.setStyleSheet("""
        QMainWindow {
            background-color: #ecf0f1;
        }
        QLabel {
            color: #2c3e50;
        }
    """)
    
    jogo = CacaPalavras()
    jogo.show()
    sys.exit(app.exec_()) 