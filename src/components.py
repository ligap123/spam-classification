import streamlit as st


def load_custom_css():
    """加载自定义 CSS 样式"""
    with open("styles.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def model_selector():
    """模型选择器组件"""
    model = st.radio(
        "选择模型",
        ["lightgbm", "logreg"],
        format_func=lambda x: "LightGBM" if x == "lightgbm" else "Logistic Regression",
        label_visibility="collapsed",
        key="model_selector"
    )
    
    # 添加模型特点描述
    st.markdown("""
    <div style="margin-top: 1rem; font-size: 0.9rem; color: var(--text-secondary);">
        <p style="font-weight: bold; margin-bottom: 0.5rem;">模型特点：</p>
        <div style="padding-left: 1rem;">
            <p><strong>LightGBM</strong> - 高效的梯度提升树模型，适合大规模数据，精度高，速度快</p>
            <p><strong>Logistic Regression</strong> - 经典的线性分类模型，训练速度快，可解释性强</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    return model


def loading_animation():
    """加载动画组件"""
    st.markdown("""
    <div class="dots-container">
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
    </div>
    """, unsafe_allow_html=True)


def result_card(prediction, analysis):
    """结果卡片组件（翻转效果）"""
    if prediction.is_spam:
        st.toast("🚨 检测到垃圾短信！", icon="⚠️")
        icon = "🚨"
        status = "垃圾短信"
        back_status = "高风险"
        back_color = "var(--danger)"
    else:
        st.toast("✅ 短信安全", icon="🛡️")
        icon = "✅"
        status = "正常短信"
        back_status = "安全"
        back_color = "var(--success)"
    
    st.markdown(f"""
    <div class="flip-card">
        <div class="flip-card-inner">
            <div class="flip-card-front">
                <h2>{icon} {status}</h2>
                <p style="font-size: 1.5rem; margin: 0.5rem 0;">
                    概率: <strong>{prediction.probability:.2%}</strong>
                </p>
                <p style="color: var(--text-secondary); margin: 0;">
                    使用模型: <strong>{prediction.model_used.upper()}</strong>
                </p>
            </div>
            <div class="flip-card-back">
                <h2>🤖 LLM 分析</h2>
                <h3>📋 摘要</h3>
                <p>{analysis.summary}</p>
                
                <h3>⚠️ 风险因素</h3>
                <ul>
    """, unsafe_allow_html=True)
    
    for factor in analysis.risk_factors:
        st.markdown(f"<li>{factor}</li>", unsafe_allow_html=True)
    
    st.markdown("""
                </ul>
                
                <h3>💡 解释</h3>
                <p>{analysis.explanation}</p>
                
                <h3>🎯 行动建议</h3>
                <p style="color: {back_color}; font-weight: 600;">{analysis.action_suggestion}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def analysis_card(analysis):
    """LLM 分析卡片组件"""
    with st.expander("🤖 LLM 分析报告", expanded=False):
        st.markdown("""
        <div class="result-card">
            <h3>📋 摘要</h3>
            <p>{analysis.summary}</p>
            
            <h3>⚠️ 风险因素</h3>
            <ul>
        """, unsafe_allow_html=True)
        
        for factor in analysis.risk_factors:
            st.markdown(f"<li>{factor}</li>", unsafe_allow_html=True)
        
        st.markdown("""
            </ul>
            
            <h3>💡 解释</h3>
            <p>{analysis.explanation}</p>
            
            <h3>🎯 行动建议</h3>
            <p style="color: var(--success); font-weight: 600;">{analysis.action_suggestion}</p>
        </div>
        """, unsafe_allow_html=True)


def comparison_card(comparison):
    """模型对比卡片组件"""
    col_a, col_b = st.columns(2)
    
    with col_a:
        logreg = comparison["logistic_regression"]
        if logreg["is_spam"]:
            st.markdown(f"""
            <div class="comparison-card result-card danger">
                <h4>Logistic Regression</h4>
                <p style="font-size: 1.3rem; margin: 0.5rem 0;">
                    🚨 垃圾短信<br>
                    <strong>{logreg['probability']:.2%}</strong>
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="comparison-card result-card success">
                <h4>Logistic Regression</h4>
                <p style="font-size: 1.3rem; margin: 0.5rem 0;">
                    ✅ 正常短信<br>
                    <strong>{logreg['probability']:.2%}</strong>
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    with col_b:
        lgb = comparison["lightgbm"]
        if lgb["is_spam"]:
            st.markdown(f"""
            <div class="comparison-card result-card danger">
                <h4>LightGBM</h4>
                <p style="font-size: 1.3rem; margin: 0.5rem 0;">
                    🚨 垃圾短信<br>
                    <strong>{lgb['probability']:.2%}</strong>
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="comparison-card result-card success">
                <h4>LightGBM</h4>
                <p style="font-size: 1.3rem; margin: 0.5rem 0;">
                    ✅ 正常短信<br>
                    <strong>{lgb['probability']:.2%}</strong>
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    if comparison["agreement"]:
        st.markdown("""
        <div class="result-card success">
            <h3>✅ 两个模型预测结果一致</h3>
            <p>判断结果可信度高，可以放心使用。</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="result-card danger">
            <h3>⚠️ 两个模型预测结果不一致</h3>
            <p>建议进一步人工审核或结合其他信息进行判断。</p>
        </div>
        """, unsafe_allow_html=True)


def tech_stack():
    """技术栈信息组件"""
    st.markdown("""
    ## 📚 技术栈
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style="margin-left: 1rem;">
        <ul>
            <li><strong>数据处理:</strong> Polars + Pandera</li>
            <li><strong>机器学习:</strong> Scikit-learn + LightGBM</li>
            <li><strong>Agent框架:</strong> Pydantic-ai</li>
            <li><strong>LLM:</strong> DeepSeek API</li>
            <li><strong>可视化:</strong> Streamlit + Seaborn</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
