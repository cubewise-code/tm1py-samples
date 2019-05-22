class Loan:

    def __init__(self, line: str):
        self.line = line.replace('"', '').replace("'", "").replace("\t", "")
        self.loan_id, self.member_id, self.loan_amnt, self.funded_amnt, self.funded_amnt_inv, self.term, \
        self.int_rate, self.installment, self.grade, self.sub_grade, self.emp_title, self.emp_length, \
        self.home_ownership, self.annual_inc, self.verification_status, self.issue_d, self.loan_status, self.pymnt_plan, \
        self.url, self.desc, self.purpose, self.title, self.zip_code, self.addr_state, self.dti, self.delinq_2yrs, \
        self.earliest_cr_line, self.fico_range_low, self.fico_range_high, self.inq_last_6mths, self.mths_since_last_delinq, self.mths_since_last_record, \
        self.open_acc, self.pub_rec, self.revol_bal, self.revol_util, self.total_acc, self.initial_list_status, \
        self.out_prncp, self.out_prncp_inv, self.total_pymnt, self.total_pymnt_inv, self.total_rec_prncp, \
        self.total_rec_int, self.total_rec_late_fee, self.recoveries, self.collection_recovery_fee, self.last_pymnt_d, \
        self.last_pymnt_amnt, self.next_pymnt_d, self.last_credit_pull_d, self.last_fico_range_high, \
        self.last_fico_range_low, self.collections_12_mths_ex_med, \
        self.mths_since_last_major_derog, self.policy_code, self.application_type, self.annual_inc_joint, \
        self.dti_joint, self.verification_status_joint, self.acc_now_delinq, self.tot_coll_amt, self.tot_cur_bal, \
        self.open_acc_6m, self.open_act_il, self.open_il_12m, self.open_il_24m, self.mths_since_rcnt_il, \
        self.total_bal_il, self.il_util, self.open_rv_12m, self.open_rv_24m, self.max_bal_bc, self.all_util, \
        self.total_rev_hi_lim, self.inq_fi, self.total_cu_tl, self.inq_last_12m, self.acc_open_past_24mths, \
        self.avg_cur_bal, self.bc_open_to_buy, self.bc_util, self.chargeoff_within_12_mths, self.delinq_amnt, \
        self.mo_sin_old_il_acct, self.mo_sin_old_rev_tl_op, self.mo_sin_rcnt_rev_tl_op, self.mo_sin_rcnt_tl, \
        self.mort_acc, self.mths_since_recent_bc, self.mths_since_recent_bc_dlq, self.mths_since_recent_inq, \
        self.mths_since_recent_revol_delinq, self.num_accts_ever_120_pd, self.num_actv_bc_tl, self.num_actv_rev_tl, \
        self.num_bc_sats, self.num_bc_tl, self.num_il_tl, self.num_op_rev_tl, self.num_rev_accts, \
        self.num_rev_tl_bal_gt_0, self.num_sats, self.num_tl_120dpd_2m, self.num_tl_30dpd, self.num_tl_90g_dpd_24m, \
        self.num_tl_op_past_12m, self.pct_tl_nvr_dlq, self.percent_bc_gt_75, self.pub_rec_bankruptcies, \
        self.tax_liens, self.tot_hi_cred_lim, self.total_bal_ex_mort, self.total_bc_limit, \
        self.total_il_high_credit_limit, self.revol_bal_joint, self.sec_app_fico_range_low, self.sec_app_fico_range_high, \
        self.sec_app_earliest_cr_line, \
        self.sec_app_inq_last_6mths, self.sec_app_mort_acc, self.sec_app_open_acc, self.sec_app_revol_util, \
        self.sec_app_open_act_il, self.sec_app_num_rev_accts, self.sec_app_chargeoff_within_12_mths, \
        self.sec_app_collections_12_mths_ex_med, self.sec_app_mths_since_last_major_derog, self.hardship_flag, \
        self.hardship_type, self.hardship_reason, self.hardship_status, self.deferral_term, self.hardship_amount, \
        self.hardship_start_date, self.hardship_end_date, self.payment_plan_start_date, self.hardship_length, \
        self.hardship_dpd, self.hardship_loan_status, self.orig_projected_additional_accrued_interest, \
        self.hardship_payoff_balance_amount, self.hardship_last_payment_amount, self.disbursement_method, \
        self.debt_settlement_flag, self.debt_settlement_flag_date, self.settlement_status, self.settlement_date, \
        self.settlement_amount, self.settlement_percentage, self.settlement_term = self.line.split(",")

        self.loan_id = "Loan " + self.loan_id

        # remove '[' and ']' from employment title
        self.emp_title = self.emp_title.replace("[", "").replace("]", "")

    def __str__(self) -> str:
        return ",".join(str(field) for field in
                        [self.loan_id,
                         self.member_id,
                         self.loan_amnt,
                         self.funded_amnt,
                         self.funded_amnt_inv,
                         self.term,
                         self.int_rate,
                         self.installment,
                         self.grade,
                         self.sub_grade,
                         self.emp_title,
                         self.emp_length,
                         self.home_ownership,
                         self.annual_inc,
                         self.verification_status,
                         self.issue_d,
                         self.loan_status,
                         self.pymnt_plan,
                         self.url,
                         self.desc,
                         self.purpose,
                         self.title,
                         self.zip_code,
                         self.addr_state,
                         self.dti,
                         self.delinq_2yrs,
                         self.earliest_cr_line,
                         self.fico_range_low,
                         self.fico_range_high,
                         self.inq_last_6mths,
                         self.mths_since_last_delinq,
                         self.mths_since_last_record,
                         self.open_acc,
                         self.pub_rec,
                         self.revol_bal,
                         self.revol_util,
                         self.total_acc,
                         self.initial_list_status,
                         self.out_prncp,
                         self.out_prncp_inv,
                         self.total_pymnt,
                         self.total_pymnt_inv,
                         self.total_rec_prncp,
                         self.total_rec_int,
                         self.total_rec_late_fee,
                         self.recoveries,
                         self.collection_recovery_fee,
                         self.last_pymnt_d,
                         self.last_pymnt_amnt,
                         self.next_pymnt_d,
                         self.last_fico_range_high,
                         self.last_fico_range_low,
                         self.last_credit_pull_d,
                         self.collections_12_mths_ex_med,
                         self.mths_since_last_major_derog,
                         self.policy_code,
                         self.application_type,
                         self.annual_inc_joint,
                         self.dti_joint,
                         self.verification_status_joint,
                         self.acc_now_delinq,
                         self.tot_coll_amt,
                         self.tot_cur_bal,
                         self.open_acc_6m,
                         self.open_act_il,
                         self.open_il_12m,
                         self.open_il_24m,
                         self.mths_since_rcnt_il,
                         self.total_bal_il,
                         self.il_util,
                         self.open_rv_12m,
                         self.open_rv_24m,
                         self.max_bal_bc,
                         self.all_util,
                         self.total_rev_hi_lim,
                         self.inq_fi,
                         self.total_cu_tl,
                         self.inq_last_12m,
                         self.acc_open_past_24mths,
                         self.avg_cur_bal,
                         self.bc_open_to_buy,
                         self.bc_util,
                         self.chargeoff_within_12_mths,
                         self.delinq_amnt,
                         self.mo_sin_old_il_acct,
                         self.mo_sin_old_rev_tl_op,
                         self.mo_sin_rcnt_rev_tl_op,
                         self.mo_sin_rcnt_tl,
                         self.mort_acc,
                         self.mths_since_recent_bc,
                         self.mths_since_recent_bc_dlq,
                         self.mths_since_recent_inq,
                         self.mths_since_recent_revol_delinq,
                         self.num_accts_ever_120_pd,
                         self.num_actv_bc_tl,
                         self.num_actv_rev_tl,
                         self.num_bc_sats,
                         self.num_bc_tl,
                         self.num_il_tl,
                         self.num_op_rev_tl,
                         self.num_rev_accts,
                         self.num_rev_tl_bal_gt_0,
                         self.num_sats,
                         self.num_tl_120dpd_2m,
                         self.num_tl_30dpd,
                         self.num_tl_90g_dpd_24m,
                         self.num_tl_op_past_12m,
                         self.pct_tl_nvr_dlq,
                         self.percent_bc_gt_75,
                         self.pub_rec_bankruptcies,
                         self.tax_liens,
                         self.tot_hi_cred_lim,
                         self.total_bal_ex_mort,
                         self.total_bc_limit,
                         self.total_il_high_credit_limit,
                         self.revol_bal_joint,
                         self.sec_app_fico_range_low,
                         self.sec_app_fico_range_high,
                         self.sec_app_earliest_cr_line,
                         self.sec_app_inq_last_6mths,
                         self.sec_app_mort_acc,
                         self.sec_app_open_acc,
                         self.sec_app_revol_util,
                         self.sec_app_open_act_il,
                         self.sec_app_num_rev_accts,
                         self.sec_app_chargeoff_within_12_mths,
                         self.sec_app_collections_12_mths_ex_med,
                         self.sec_app_mths_since_last_major_derog,
                         self.hardship_flag,
                         self.hardship_type,
                         self.hardship_reason,
                         self.hardship_status,
                         self.deferral_term,
                         self.hardship_amount,
                         self.hardship_start_date,
                         self.hardship_end_date,
                         self.payment_plan_start_date,
                         self.hardship_length,
                         self.hardship_dpd,
                         self.hardship_loan_status,
                         self.orig_projected_additional_accrued_interest,
                         self.hardship_payoff_balance_amount,
                         self.hardship_last_payment_amount,
                         self.disbursement_method,
                         self.debt_settlement_flag,
                         self.debt_settlement_flag_date,
                         self.settlement_status,
                         self.settlement_date,
                         self.settlement_amount,
                         self.settlement_percentage,
                         self.settlement_term])

    def determine_fico_score(self):
        if not self.fico_range_low and self.fico_range_high:
            return str(int(float(self.fico_range_low)))
        if self.fico_range_low and not self.fico_range_high:
            return str(int(float(self.fico_range_high)))
        if not self.fico_range_low and not self.fico_range_high:
            return "350"
        return str(int((float(self.fico_range_low) + float(self.fico_range_high)) / 2))

    def determine_income_class(self):
        if self.verification_status in ('', 'Not Verified'):
            return "10000"
        annual_income = float(self.annual_inc.replace('"', ''))
        if annual_income < 10000:
            return "10000"
        if annual_income < 20000:
            return "20000"
        if annual_income < 30000:
            return "30000"
        if annual_income < 40000:
            return "40000"
        if annual_income < 50000:
            return "50000"
        if annual_income < 60000:
            return "60000"
        if annual_income < 70000:
            return "70000"
        if annual_income < 80000:
            return "80000"
        if annual_income < 90000:
            return "90000"
        if annual_income < 100000:
            return "100000"
        if annual_income < 110000:
            return "110000"
        if annual_income < 120000:
            return "120000"
        if annual_income < 130000:
            return "130000"
        if annual_income < 140000:
            return "140000"
        if annual_income < 150000:
            return "150000"
        if annual_income < 160000:
            return "160000"
        if annual_income < 170000:
            return "170000"
        if annual_income < 180000:
            return "180000"
        else:
            return "190000"

    def generate_cells(self) -> dict:
        cells = dict()
        # if dti missing return empty dict
        if not self.dti:
            return cells

        coordinates_without_measure = (
            self.issue_d,
            self.loan_id,
            self.sub_grade,
            self.determine_fico_score(),
            self.emp_title.replace("[", "").replace("]", "") if self.emp_title else "None",
            self.term,
            self.determine_income_class(),
            self.purpose,
            self.loan_status,
            self.addr_state,
            self.home_ownership,
            self.application_type,
            str(int(float(self.delinq_2yrs))),
            "%.2f" % float(self.dti))
        cells[coordinates_without_measure + ("loan_amnt",)] = self.loan_amnt
        cells[coordinates_without_measure + ("int_rate",)] = float(self.int_rate) / 100
        cells[coordinates_without_measure + ("installment",)] = self.installment
        cells[coordinates_without_measure + ("out_prncp",)] = self.out_prncp
        cells[coordinates_without_measure + ("total_pymnt",)] = self.total_pymnt
        cells[coordinates_without_measure + ("last_pymnt_d",)] = self.last_pymnt_d
        cells[coordinates_without_measure + ("last_pymnt_amnt",)] = self.last_pymnt_amnt
        emp_length = ''.join(filter(lambda x: x.isdigit(), self.emp_length))
        cells[coordinates_without_measure + ("emp_length",)] = emp_length if emp_length else 0
        cells[coordinates_without_measure + ("num_personal_inquiries",)] = self.inq_fi if self.inq_fi else 0
        cells[coordinates_without_measure + ("inquiries_in_last_12m",)] = self.inq_last_12m if self.inq_last_12m else 0
        cells[coordinates_without_measure + (
            "mths_since_last_delinq",)] = self.mths_since_last_delinq if self.mths_since_last_delinq else 240
        cells[coordinates_without_measure + (
            "mths_since_recent_bc_dlq",)] = self.mths_since_recent_bc_dlq if self.mths_since_recent_bc_dlq else 240
        cells[coordinates_without_measure + (
            "mths_since_recent_inq",)] = self.mths_since_recent_inq if self.mths_since_recent_inq else 240
        cells[coordinates_without_measure + (
            "mths_since_recent_revol_delinq",)] = self.mths_since_recent_revol_delinq if self.mths_since_recent_revol_delinq else 240

        return cells
