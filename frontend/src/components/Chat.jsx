import { useState, useRef, useEffect } from 'react';
import chatbotApi from '../config/chatbotApi';
import { MessageCircle, Plus, Send, Sparkles, HelpCircle, Lightbulb, Bot, User } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import './Chat.css';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [threadId, setThreadId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async (e) => {
    e.preventDefault();
    
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    
    setMessages(prev => [...prev, { 
      type: 'user', 
      content: userMessage 
    }]);

    setIsLoading(true);

    try {
      const response = await chatbotApi.post('/chat/', {
        user_message: userMessage,
        thread_id: threadId
      });

      const { thread_id, ai_message } = response.data;
      
      if (!threadId) {
        setThreadId(thread_id);
      }

      setMessages(prev => [...prev, { 
        type: 'ai', 
        content: ai_message 
      }]);

    } catch (error) {
      console.error('Erro ao enviar mensagem:', error);
      
      let errorMessage = 'Desculpe, ocorreu um erro ao processar sua mensagem. Tente novamente.';
      
      if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
        errorMessage = '⏱️ A requisição demorou muito tempo. O processamento pode estar complexo. Tente novamente.';
      } else if (error.response?.status === 500) {
        errorMessage = '🔧 Erro no servidor. Tente novamente em instantes.';
      } else if (!error.response) {
        errorMessage = '🌐 Não foi possível conectar ao servidor. Verifique sua conexão.';
      }
      
      setMessages(prev => [...prev, { 
        type: 'error', 
        content: errorMessage
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([]);
    setThreadId(null);
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <div className="header-content">
          <div className="header-title">
            <div className="icon-wrapper">
              <MessageCircle size={28} strokeWidth={2} />
            </div>
            <div>
              <h1>Assistente Virtual</h1>
              <span className="status">Online</span>
            </div>
          </div>
          {messages.length > 0 && (
            <button onClick={clearChat} className="clear-btn" title="Nova conversa">
              <Plus size={18} />
              Nova conversa
            </button>
          )}
        </div>
      </div>

      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="welcome-screen">
            <div className="welcome-icon">
              <Sparkles size={64} strokeWidth={1.5} className="sparkle-icon" />
            </div>
            <h2>Olá! Como posso ajudar?</h2>
            <p>Faça uma pergunta ou inicie uma conversa</p>
            <div className="suggestion-chips">
              <button onClick={() => setInputMessage('Olá!')} className="chip">
                <MessageCircle size={16} />
                Começar conversa
              </button>
              <button onClick={() => setInputMessage('Como você funciona?')} className="chip">
                <HelpCircle size={16} />
                Como funciona
              </button>
              <button onClick={() => setInputMessage('Me ajude com algo')} className="chip">
                <Lightbulb size={16} />
                Preciso de ajuda
              </button>
            </div>
          </div>
        ) : (
          <>
            {messages.map((message, index) => (
              <div key={index} className={`message-wrapper message-${message.type}`}>
                <div className="message-bubble">
                  {message.type === 'ai' && (
                    <div className="avatar avatar-ai">
                      <Bot size={20} strokeWidth={2} />
                    </div>
                  )}
                  <div className="message-content">
                    {message.type === 'ai' ? (
                      <ReactMarkdown 
                        remarkPlugins={[remarkGfm]}
                        components={{
                          // Customiza os elementos do markdown
                          p: ({node, ...props}) => <p style={{marginBottom: '0.75rem'}} {...props} />,
                          ul: ({node, ...props}) => <ul style={{marginLeft: '1.25rem', marginBottom: '0.75rem'}} {...props} />,
                          ol: ({node, ...props}) => <ol style={{marginLeft: '1.25rem', marginBottom: '0.75rem'}} {...props} />,
                          li: ({node, ...props}) => <li style={{marginBottom: '0.25rem'}} {...props} />,
                          code: ({node, inline, ...props}) => 
                            inline 
                              ? <code style={{background: 'rgba(0,0,0,0.1)', padding: '0.125rem 0.375rem', borderRadius: '3px', fontSize: '0.875em'}} {...props} />
                              : <code style={{display: 'block', background: 'rgba(0,0,0,0.05)', padding: '0.75rem', borderRadius: '6px', overflowX: 'auto', fontSize: '0.875em'}} {...props} />,
                          strong: ({node, ...props}) => <strong style={{fontWeight: '700'}} {...props} />,
                          em: ({node, ...props}) => <em style={{fontStyle: 'italic'}} {...props} />,
                          h1: ({node, ...props}) => <h1 style={{fontSize: '1.5rem', fontWeight: '700', marginBottom: '0.75rem'}} {...props} />,
                          h2: ({node, ...props}) => <h2 style={{fontSize: '1.25rem', fontWeight: '700', marginBottom: '0.5rem'}} {...props} />,
                          h3: ({node, ...props}) => <h3 style={{fontSize: '1.1rem', fontWeight: '600', marginBottom: '0.5rem'}} {...props} />,
                        }}
                      >
                        {message.content}
                      </ReactMarkdown>
                    ) : (
                      message.content
                    )}
                  </div>
                  {message.type === 'user' && (
                    <div className="avatar avatar-user">
                      <User size={20} strokeWidth={2} />
                    </div>
                  )}
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="message-wrapper message-ai">
                <div className="message-bubble">
                  <div className="avatar avatar-ai">
                    <Bot size={20} strokeWidth={2} />
                  </div>
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
          </>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-container">
        <form onSubmit={sendMessage} className="chat-input-form">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Digite sua mensagem..."
            disabled={isLoading}
            className="chat-input"
          />
          <button 
            type="submit" 
            disabled={isLoading || !inputMessage.trim()}
            className="send-btn"
            title="Enviar mensagem"
          >
            <Send size={20} strokeWidth={2} />
          </button>
        </form>
      </div>
    </div>
  );
};

export default Chat;