import streamlit as st
import pandas as pd
import statsmodels.api as sm


def perform_logistic_regression(df, variables, confidence_level):
    X = df[variables]
    X = sm.add_constant(X)
    y = df['case']

    model = sm.Logit(y, X).fit()
    alpha = 1 - confidence_level
    ci = model.conf_int(alpha=alpha)  # 根据置信水平计算置信区间
    return model.params, ci


def run():
    st.title("Confounding 分析器")

    uploaded_file = st.file_uploader("上传一个CSV文件-3", type=['csv'])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write(df.head())

        # 获取所有列名
        columns = list(df.columns)
        columns.remove('case')  # 移除因变量

        # 让用户选择自变量和可能的混杂因子
        common_var = st.selectbox(
            "选择两次都使用的自变量", columns, index=columns.index('estro'))
        confounder_vars = st.multiselect(
            "选择第二次逻辑回归中加入的可能的混杂因子", [col for col in columns if col != common_var], default=['obesity'])

        # 获取阈值
        threshold = st.slider("选择混杂效应的阈值", 0.01, 1.00, 0.10)

        # 让用户选择置信水平
        confidence_level = st.slider("选择置信水平", 0.80, 0.99, 0.95)

        if st.button("查看结果"):
            # 单变量逻辑回归
            st.subheader("第一次逻辑回归")
            first_regression_params, _ = perform_logistic_regression(
                df, [common_var], confidence_level)
            st.write(
                f"主要自变量系数 (不考虑可能的混杂因子): {first_regression_params[common_var]:.4f}")

            # 考虑可能的混杂因子
            st.subheader("第二次逻辑回归")
            second_regression_params, ci = perform_logistic_regression(
                df, [common_var] + confounder_vars, confidence_level)
            st.write(
                f"主要自变量系数 (考虑可能的混杂因子): {second_regression_params[common_var]:.4f}")

            # 判断混杂效应
            change = abs(
                second_regression_params[common_var] - first_regression_params[common_var])

            change_threshold = threshold * \
                abs(first_regression_params[common_var])

            if change > change_threshold:
                st.warning(
                    f"{', '.join(confounder_vars)}可能是混杂因子。系数变化: {change:.4f}，超过设定的阈值（{change_threshold:.4f}）。"
                    f"原始系数为: {first_regression_params[common_var]:.4f}，加入混杂因子后系数为: {second_regression_params[common_var]:.4f}。"
                )
            else:
                st.success(
                    f"{', '.join(confounder_vars)}可能不是混杂因子。系数变化: {change:.4f}，未超过设定的阈值（{change_threshold:.4f}）。"
                    f"原始系数为: {first_regression_params[common_var]:.4f}，加入混杂因子后系数为: {second_regression_params[common_var]:.4f}。"
                )

            # 根据用户选择的置信水平提取相应的置信区间并显示
            _, ci = perform_logistic_regression(
                df, [common_var] + confounder_vars, confidence_level)
            lower, upper = ci.loc[common_var]
            st.write(
                f"{confidence_level*100:.1f}%置信区间为: ({lower:.4f}, {upper:.4f})")
            if lower > 1 or upper < 1:
                st.write(
                    f"在{confidence_level*100:.1f}%的置信水平下，雌激素用户与非雌激素用户间患子宫内膜癌的几率是显著不同的。")
            else:
                st.write(
                    f"在{confidence_level*100:.1f}%的置信水平下，雌激素用户与非雌激素用户间患子宫内膜癌的几率没有显著差异。")
