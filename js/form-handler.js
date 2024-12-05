class FormHandler {
    constructor() {
        this.form = document.getElementById('inscricaoForm');
        this.progressBar = document.querySelector('.progress-bar');
        this.inputs = this.form.querySelectorAll('input[required]');
        this.setupListeners();
    }

    setupListeners() {
        // Atualizar progresso quando qualquer input mudar
        this.inputs.forEach(input => {
            input.addEventListener('input', () => this.updateProgress());
            input.addEventListener('change', () => this.updateProgress());
        });

        // Gerenciar envio do formulário
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
    }

    updateProgress() {
        const total = Array.from(this.inputs).filter(input => input.hasAttribute('required')).length;
        let filled = 0;

        this.inputs.forEach(input => {
            if (!input.hasAttribute('required')) return; // Ignora campos opcionais
            if (input.type === 'file' && input.files.length > 0) filled++;
            else if (input.type !== 'file' && input.value.trim() !== '') filled++;
        });

        const percentage = Math.round((filled / total) * 100);
        this.progressBar.style.width = `${percentage}%`;
        this.progressBar.textContent = `${percentage}%`;
        this.progressBar.setAttribute('aria-valuenow', percentage);
    }

    async handleSubmit(event) {
        event.preventDefault();

        // Coletar dados do formulário
        const formData = new FormData(this.form);
        
        try {
            // Simular envio para o servidor
            await this.simulateServerRequest(formData);
            
            // Enviar e-mail de confirmação
            await this.sendConfirmationEmail(formData);
            
            // Mostrar mensagem de sucesso
            Swal.fire({
                title: 'Sucesso!',
                text: 'Inscrição realizada com sucesso! Verifique seu e-mail para a confirmação.',
                icon: 'success',
                confirmButtonColor: '#00c7ec'
            });
            
            this.form.reset();
            this.updateProgress();
            
        } catch (error) {
            Swal.fire({
                title: 'Erro!',
                text: 'Ocorreu um erro ao processar sua inscrição. Tente novamente.',
                icon: 'error',
                confirmButtonColor: '#00c7ec'
            });
        }
    }

    async simulateServerRequest(formData) {
        // Simular delay de processamento
        await new Promise(resolve => setTimeout(resolve, 1500));
        return true;
    }

    async sendConfirmationEmail(formData) {
        // Aqui você implementaria a lógica real de envio de e-mail
        // Por enquanto, vamos apenas simular
        const emailTemplate = `
            Olá ${formData.get('nome')},
            
            Sua inscrição foi recebida com sucesso!
            
            Dados da inscrição:
            - Nome: ${formData.get('nome')}
            - CPF: ${formData.get('cpf')}
            - Email: ${formData.get('email')}
            - Telefone: ${formData.get('telefone')}
            
            Em breve entraremos em contato para os próximos passos.
            
            Atenciosamente,
            Equipe TechDev
        `;
        
        console.log('E-mail enviado:', emailTemplate);
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    new FormHandler();
}); 