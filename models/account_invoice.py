from odoo import models, api, _


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def action_invoice_sent(self):
        """ Open a window to compose an email, with the edi invoice template
            message loaded by default
        """
        self.ensure_one()
        template = self.env.ref('account.email_template_edi_invoice', False)
        compose_form = self.env.ref(
            'mail.email_compose_message_wizard_form', False)
        ctx = dict(
            default_model='account.invoice',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode='comment',
            mark_invoice_as_sent=True,
            custom_layout="account.mail_template_data_notification_email_account_invoice",
            force_email=True
        )
        # Begin modification
        attachments = self.env['ir.attachment']
        attachs = attachments.search([
            ('res_model', '=', self._name),
            ('res_id', '=', self.id)])
        name = ''
        for attach in attachs:
            name = attach.name
            if name.upper()[:3] == 'FAC':
                attachs.search([('id', '=', attach.id)]).unlink()

        # self.env['ir.attachment'].search([
        #     ('res_model', '=', self._name),
        #     ('res_id', '=', self.id),
        #     ('name', 'like', 'Fac%')
        # ]).unlink()
        # End modification
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }
