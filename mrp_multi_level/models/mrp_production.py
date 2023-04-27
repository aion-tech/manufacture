# Copyright 2020 ForgeFlow S.L. (https://www.forgeflow.com)
# - Héctor Villarreal <hector.villarreal@forgeflow.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


class MrpProduction(models.Model):
    """Manufacturing Orders"""

    _inherit = "mrp.production"

    planned_order_id = fields.Many2one(comodel_name="mrp.planned.order")
    origin_sale_order_ids = fields.Many2many(
        "sale.order",
        string="Origin Sale Orders",
        readonly=True,
    )
    origin_sale_order_ids_count = fields.Integer(
        string="Origin Sale Orders Count",
        compute="_compute_origin_sale_order_ids_count",
    )
    llc = fields.Integer(string="Low Level Code", related="product_id.llc", store=True)

    def _compute_origin_sale_order_ids_count(self):
        for record in self:
            record.origin_sale_order_ids_count = len(record.origin_sale_order_ids)

    def action_view_origin_sale_order_ids(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "MRP sale orders",
            "view_mode": "tree,form",
            "res_model": "sale.order",
            "domain": [("id", "in", self.origin_sale_order_ids.ids)],
            "context": "{'create': False}",
        }
