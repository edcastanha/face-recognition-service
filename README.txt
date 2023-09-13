   matchDia = re.search(r'(\d{4}-\d{2}-\d{2})', directory)
                    if matchDia:
                        self.dia_captura = matchDia.group(1)
                        # Extrair a hora
                        matchHora = re.search(r'\d{4}-\d{2}-\d{2}/\d{3}/jpg/(\d{2})/(\d{2})\.(\d{2})', 
                        directory)
                    if matchHora:
                        self.hora_captura = f"{matchHora.group(1)}:{matchHora.group(2)}:
                        {matchHora.group(3)}"