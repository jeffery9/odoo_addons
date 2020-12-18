# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

import json
from datetime import timedelta

import requests
from odoo import api, fields, models
from odoo.exceptions import UserError


class wxworkCheckin(models.Model):
    _name = 'wxwork.checkin'
    _description = 'wxwork Checkin Data'

    _rec_name = 'checkin_time'
    _order = 'checkin_time ASC'

    userid = fields.Char(string=u'Userid', )

    groupname = fields.Char(string=u'Groupname', )

    checkin_type = fields.Char(string=u'Checkin Type', )

    exception_type = fields.Char(string=u'Exception Type', )

    checkin_time = fields.Integer(string=u'Checkin Time', )

    location_title = fields.Char(string=u'Location Title', )

    location_detail = fields.Char(string=u'Location Detail', )

    wifiname = fields.Char(string=u'Wifiname', )

    notes = fields.Char(string=u'Notes', )

    wifimac = fields.Char(string=u'Wifimac', )

    sch_checkin_time = fields.Integer(string=u'Sch Checkin Time', )

    groupid = fields.Char(string=u'Groupid', )

    schedule_id = fields.Char(string=u'Schedule Id', )

    timeline_id = fields.Char(string=u'Timeline Id', )

    employee_id = fields.Many2one(string=u'Employee',
                                  comodel_name='hr.employee',
                                  ondelete='restrict',
                                  compute='_compute_employee_id',
                                  store=True)

    group_id = fields.Many2one(string=u'Checkin Group',
                               comodel_name='wxwork.checkin.group',
                               ondelete='restrict',
                               compute='_compute_group_id',
                               store=True)

    @api.depends('groupid')
    def _compute_group_id(self):
        for record in self:
            record.group_id = self.env['wxwork.checkin.group'].search(
                [('groupid', '=', record.group)], limit=1).id

    @api.depends('userid')
    def _compute_employee_id(self):
        for record in self:
            record.employee_id = self.env['hr.employee'].search([
                ('wxwork_userid', '=', record.userid)
            ]).id


class wxworkCheckinGroup(models.Model):
    _name = 'wxwork.checkin.group'
    _description = 'wxwork Checkin Group'

    _rec_name = 'groupname'
    _order = 'groupname ASC'

    employee_ids = fields.Many2many(
        string=u'Employee',
        comodel_name='hr.employee',
        relation='wxwork_checkin_group_employee_rel',
        column1='employee_id',
        column2='group_id',
    )

    grouptype = fields.Selection(string=u'Group Type',
                                 selection=[('fixed', 'Fixed'),
                                            ('shift', 'Shifted'),
                                            ('flexible', 'Flexible')],
                                 default='fixed')

    groupid = fields.Char(string=u'Group id', )

    groupname = fields.Char(string=u'Group Name', )

    checkin_date_ids = fields.One2many(
        string=u'Checkin Date',
        comodel_name='wxwork.checkin.date',
        inverse_name='checkin_group_id',
    )

    spe_workday_ids = fields.One2many(string=u'spe_workday',
                                      comodel_name='wxwork.checkin.spe_day',
                                      inverse_name='checkin_group_id',
                                      domain=[('spe_type', '=', 'workday')])

    spe_offday_ids = fields.One2many(string=u'spe_offday',
                                     comodel_name='wxwork.checkin.spe_day',
                                     inverse_name='checkin_group_id',
                                     domain=[('spe_type', '=', 'offday')])

    loc_info_ids = fields.One2many(
        string=u'loc_info',
        comodel_name='wxwork.checkin.loc_info',
        inverse_name='checkin_group_id',
    )

    schedule_ids = fields.One2many(
        string=u'schedule',
        comodel_name='wxwork.checkin.schedule',
        inverse_name='checkin_group_id',
    )

    json_data = fields.Text(string='Json Data', readonly=True)


class wxworkCheckinDate(models.Model):
    _name = 'wxwork.checkin.date'
    _description = 'wxwork Checkin Date'

    _rec_name = 'name'
    _order = 'name ASC'

    checkin_group_id = fields.Many2one(
        string=u'Checkin Group',
        comodel_name='wxwork.checkin.group',
        ondelete='restrict',
    )

    name = fields.Char(string=u'Name', required=True, copy=False)

    mon = fields.Boolean(string=u'Mon', )

    tue = fields.Boolean(string=u'Tue', )

    wed = fields.Boolean(string=u'Wed', )

    thu = fields.Boolean(string=u'Thu', )

    fri = fields.Boolean(string=u'Fri', )

    sat = fields.Boolean(string=u'Sat', )

    sun = fields.Boolean(string=u'Sun', )

    checkin_time_ids = fields.Many2many(
        string=u'Checkin Time',
        comodel_name='wxwork.checkin.time',
        relation='wxwork_checkin_time_date_rel',
        column1='time_id',
        column2='date_id',
    )

    flex_time = fields.Integer(string=u'Flex Time')

    noneed_offwork = fields.Boolean(string=u'No Need Offwork', )

    limit_aheadtime = fields.Integer(string=u'Limit Ahead Time', )


class wxworkCheckinTime(models.Model):
    _name = 'wxwork.checkin.time'
    _description = 'wxwork Checkin Time'

    name = fields.Char(string=u'Name', required=True, copy=False)

    work_sec = fields.Integer(string=u'Work Sec', )

    off_work_sec = fields.Integer(string=u'Off Work Sec', )

    remind_work_sec = fields.Integer(string=u'Remind Work Sec', )

    remind_off_work_sec = fields.Integer(string=u'Remind Off Work Sec', )

    _sql_constraints = [('unique_name', 'unique(name)',
                         'the name muse be unique!')]


class wxworkCheckinSpeday(models.Model):
    _name = 'wxwork.checkin.spe_day'
    _description = 'wxwork Checkin spe_day'
    _rec_name = 'timestamp'

    checkin_group_id = fields.Many2one(
        string=u'Checkin Group',
        comodel_name='wxwork.checkin.group',
        ondelete='restrict',
    )

    timestamp = fields.Integer(string=u'Timestamp', )

    spe_type = fields.Selection(string=u'Spe Type',
                                selection=[('workday', 'Workday'),
                                           ('offday', 'Offday')],
                                required=True)

    notes = fields.Char(string=u'Notes', )

    checkin_time_ids = fields.Many2many(
        string=u'Checkin Time',
        comodel_name='wxwork.checkin.time',
        relation='wxwork_checkin_time_spe_workday_rel',
        column1='time_id',
        column2='spe_workday_id',
    )


class wxworkCheckinLocinfo(models.Model):
    _name = 'wxwork.checkin.loc_info'
    _description = 'wxwork Checkin loc_info'
    _rec_name = 'loc_detail'

    checkin_group_id = fields.Many2one(
        string=u'Checkin Group',
        comodel_name='wxwork.checkin.group',
        ondelete='restrict',
    )

    lat = fields.Integer(string=u'Lat', )

    lng = fields.Integer(string=u'Lng', )

    loc_title = fields.Char(string=u'Loc Title', )

    loc_detail = fields.Char(string=u'Loc Detail', )

    distance = fields.Integer(string=u'Distance', )


class wxworkCheckinSchedule(models.Model):
    _name = 'wxwork.checkin.schedule'
    _description = 'wxwork Checkin schedule'
    _rec_name = 'schedule_name'

    checkin_group_id = fields.Many2one(
        string=u'Checkin Group',
        comodel_name='wxwork.checkin.group',
        ondelete='restrict',
    )

    schedule_id = fields.Char(string=u'Schedule Id', )

    schedule_name = fields.Char(string=u'Schedule Name', )

    time_section_ids = fields.One2many(
        string=u'Time Section',
        comodel_name='wxwork.checkin.schedule.time_section',
        inverse_name='schedule_id',
    )

    noneed_offwork = fields.Boolean(string=u'No Need Offwork', )

    limit_aheadtime = fields.Integer(string=u'Limit Ahead Time', )

    limit_offtime = fields.Integer(string=u'Limit Offtime', )

    flex_on_duty_time = fields.Integer(string=u'Flex On Duty Time', )

    flex_off_duty_time = fields.Integer(string=u'Flex Off Duty Time', )

    allow_flex = fields.Boolean(string=u'Allow Flex', )

    max_allow_arrive_early = fields.Integer(string=u'Max Allow Arrive Early', )

    max_allow_arrive_late = fields.Integer(string=u'Max Allow Arrive Late', )


class wxworkCheckinScheduleTimesection(models.Model):
    _name = 'wxwork.checkin.schedule.time_section'
    _description = 'wxwork Checkin Schedule Time_section'

    schedule_id = fields.Many2one(
        string=u'Schedule',
        comodel_name='wxwork.checkin.schedule',
        ondelete='restrict',
    )

    time_id = fields.Integer(string=u'Time Id', )

    work_sec = fields.Integer(string=u'Work Sec', )

    off_work_sec = fields.Integer(string=u'Off Work Sec', )

    remind_work_sec = fields.Integer(string=u'Remind Work Sec', )

    remind_off_work_sec = fields.Integer(string=u'Remind off Work Sec', )

    rest_begin_time = fields.Integer(string=u'Rest Begin Time', )

    rest_end_time = fields.Integer(string=u'Rest End Time', )

    allow_rest = fields.Integer(string=u'Allow Rest', )


class wxworkCheckinScheduleLaterule(models.Model):
    _name = 'wxwork.checkin.schedule.late_rule'
    _description = 'wxwork Checkin Schedule late_rule'

    allow_offwork_after_time = fields.Boolean(
        string=u'Allow Offwork After Time', )

    timerule_ids = fields.One2many(
        comodel_name='wxwork.checkin.schedule.late_rule.timerule',
        inverse_name='late_rule_id',
        string='late time rule')


class wxworkCheckinScheduleLateruleTimerule(models.Model):
    _name = 'wxwork.checkin.schedule.late_rule.timerule'
    _description = 'New Description'

    offwork_after_time = fields.Integer()

    onwork_flex_time = fields.Integer()

    late_rule_id = fields.Many2one(
        comodel_name='wxwork.checkin.schedule.late_rule')
