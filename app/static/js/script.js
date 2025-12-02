// 全局脚本：增强用户体验
document.addEventListener('DOMContentLoaded', function() {
    // 自动关闭alert提示（3秒后）
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 3000);
    });

    // 表单提交加载状态
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> 处理中...';
            }
        });
    });

    // 日期时间选择器优化（确保截止日期不晚于比赛日期）
    const startDateInput = document.querySelector('input[name="start_date"]');
    const deadlineInput = document.querySelector('input[name="application_deadline"]');

    if (startDateInput && deadlineInput) {
        startDateInput.addEventListener('change', function() {
            deadlineInput.max = this.value;
        });
    }

    // 参赛类型切换（团队/个人）
    const teamNameInput = document.querySelector('input[name="team_name"]');
    if (teamNameInput) {
        const competitionSelect = document.querySelector('select[name="competition_id"]');
        if (competitionSelect) {
            competitionSelect.addEventListener('change', function() {
                const selectedOption = this.options[this.selectedIndex];
                const category = selectedOption.textContent.includes('团队') ? '团队' : '个人';
                if (category === '个人') {
                    teamNameInput.value = '';
                    teamNameInput.disabled = true;
                    teamNameInput.placeholder = '个人参赛无需填写';
                } else {
                    teamNameInput.disabled = false;
                    teamNameInput.placeholder = '请输入团队名称';
                }
            });
        }
    }
});