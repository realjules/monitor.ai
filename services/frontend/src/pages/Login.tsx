import React, { useState } from 'react';
import {
  Box,
  Button,
  TextField,
  Typography,
  IconButton,
  InputAdornment,
  Container,
  Paper,
  Alert,
  Checkbox,
  FormControlLabel,
  Divider,
  useTheme,
  useMediaQuery,
  Stack
} from '@mui/material';
import { Link, useNavigate } from 'react-router-dom';
import { styled } from '@mui/material/styles';
import { useAuth } from '../contexts/AuthContext';
import { 
  ArrowBack, 
  Visibility, 
  VisibilityOff,
  Google as GoogleIcon,
  GitHub as GitHubIcon,
  LinkedIn as LinkedInIcon
} from '@mui/icons-material';

// Custom styled components
const StyledPaper = styled(Paper)(({ theme }) => ({
  width: '100%',
  maxWidth: '400px',
  padding: theme.spacing(4),
  borderRadius: '25px',
  boxShadow: '0 10px 30px rgba(0, 0, 0, 0.1)',
  position: 'relative',
  zIndex: 2,
  [theme.breakpoints.down('sm')]: {
    padding: theme.spacing(3),
    borderRadius: '15px',
    maxWidth: '100%',
  },
}));

const GradientOverlay = styled(Box)({
  position: 'absolute',
  right: 0,
  width: '50%', 
  height: '100%',
  background: 'linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,152,0,0.2) 100%)',
  zIndex: 0,
});

const StyledButton = styled(Button)(({ theme }) => ({
  borderRadius: '50px',
  padding: '10px 0',
  backgroundColor: '#000',
  color: 'white',
  fontWeight: 'bold',
  textTransform: 'none',
  '&:hover': {
    backgroundColor: '#333',
  },
}));

const StyledTextField = styled(TextField)(({ theme }) => ({
  marginBottom: theme.spacing(2),
  '& .MuiOutlinedInput-root': {
    '& fieldset': {
      borderColor: '#ddd',
      borderRadius: '8px',
    },
    '&:hover fieldset': {
      borderColor: '#aaa',
    },
    '&.Mui-focused fieldset': {
      borderColor: '#ff9800',
    },
  },
  '& .MuiInputLabel-root': {
    color: '#666',
  },
  '& .MuiInputLabel-root.Mui-focused': {
    color: '#ff9800',
  },
}));

const UserAvatar = styled('div')(({ theme }) => ({
  width: '60px',
  height: '60px',
  borderRadius: '50%',
  backgroundColor: '#f0f0f0',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  margin: '0 auto 20px',
  [theme.breakpoints.down('sm')]: {
    width: '50px',
    height: '50px',
  },
}));

const UserIcon = () => (
  <svg width="30" height="30" viewBox="0 0 24 24" fill="#333">
    <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" />
  </svg>
);

const DotPattern = styled('div')({
  position: 'absolute',
  width: '80px',
  height: '80px',
  right: '15px',
  top: '15px',
  opacity: 0.4,
  backgroundImage: 'radial-gradient(#ff9800 2px, transparent 2px)',
  backgroundSize: '10px 10px',
});

// Animated elements for right panel
const FloatingLine = styled('div')(({ width, top, left, color = '#FF9800', rotate = 0, delay = 0 }) => ({
  position: 'absolute',
  width,
  height: '4px',
  backgroundColor: color,
  borderRadius: '4px',
  top,
  left,
  transform: `rotate(${rotate}deg)`,
  opacity: 0.8,
  '@keyframes float': {
    '0%': {
      transform: `translateY(0) rotate(${rotate}deg)`,
    },
    '50%': {
      transform: `translateY(-10px) rotate(${rotate}deg)`,
    },
    '100%': {
      transform: `translateY(0) rotate(${rotate}deg)`,
    },
  },
  animation: 'float 6s ease-in-out infinite',
  animationDelay: `${delay}s`,
}));

const FloatingCircle = styled('div')(({ size, top, left, color = '#FF9800', opacity = 0.7, delay = 0 }) => ({
  position: 'absolute',
  width: size,
  height: size,
  borderRadius: '50%',
  backgroundColor: color,
  top,
  left,
  opacity,
  '@keyframes floatCircle': {
    '0%': {
      transform: 'translateY(0)',
    },
    '50%': {
      transform: 'translateY(-15px)',
    },
    '100%': {
      transform: 'translateY(0)',
    },
  },
  animation: 'floatCircle 7s ease-in-out infinite',
  animationDelay: `${delay}s`,
}));

const FloatingSquare = styled('div')(({ size, top, left, color = '#FF9800', delay = 0 }) => ({
  position: 'absolute',
  width: size,
  height: size,
  backgroundColor: color,
  borderRadius: '4px',
  top,
  left,
  '@keyframes floatSquare': {
    '0%': {
      transform: 'translateY(0) rotate(0deg)',
    },
    '50%': {
      transform: 'translateY(-10px) rotate(10deg)',
    },
    '100%': {
      transform: 'translateY(0) rotate(0deg)',
    },
  },
  animation: 'floatSquare 8s ease-in-out infinite',
  animationDelay: `${delay}s`,
}));

export const Login: React.FC = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const isSmall = useMediaQuery(theme.breakpoints.down('sm'));
  
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleClickShowPassword = () => {
    setShowPassword(!showPassword);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    if (!username || !password) {
      setError('Please enter both username and password');
      return;
    }
    
    try {
      setIsLoading(true);
      await login(username, password);
      navigate('/dashboard');
    } catch (err) {
      setError('Invalid username or password');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        width: '100%',
        position: 'relative',
        overflow: 'hidden',
        flexDirection: { xs: 'column', md: 'row' }
      }}
    >
      {/* Left side with orange background and login card */}
      <Box
        sx={{
          width: { xs: '100%', md: '40%' },
          minWidth: { xs: '100%', md: '380px' },
          maxWidth: { xs: '100%', md: '500px' },
          background: 'linear-gradient(135deg, #FFA726 0%, #FF7043 100%)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          position: 'relative',
          padding: { xs: 2, sm: 3, md: 4 },
          minHeight: { xs: 'auto', md: '100vh' },
          py: { xs: 4, md: 0 }
        }}
      >
        <StyledPaper elevation={3}>
          <Box sx={{ position: 'absolute', top: { xs: 8, sm: 16 }, left: { xs: 8, sm: 16 } }}>
            <IconButton 
              onClick={() => navigate('/')}
              size={isSmall ? "small" : "medium"}
              sx={{ color: '#666' }}
            >
              <ArrowBack fontSize={isSmall ? "small" : "medium"} />
            </IconButton>
          </Box>
          
          <DotPattern />
          
          <Box sx={{ textAlign: 'center', mb: { xs: 2, sm: 4 } }}>
            <UserAvatar>
              <UserIcon />
            </UserAvatar>
            <Typography variant="h6" sx={{ fontWeight: 500, color: '#333', fontSize: { xs: '1rem', sm: '1.25rem' } }}>
              Welcome Back!
            </Typography>
          </Box>
          
          {error && (
            <Alert 
              severity="error" 
              sx={{ 
                mb: 2, 
                borderRadius: '8px',
                fontSize: { xs: '0.75rem', sm: '0.875rem' }
              }}
            >
              {error}
            </Alert>
          )}

          <Box component="form" onSubmit={handleSubmit}>
            <StyledTextField
              fullWidth
              variant="outlined"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Username"
              size={isSmall ? "small" : "medium"}
              margin="normal"
              InputProps={{
                style: { 
                  fontSize: isSmall ? '13px' : '14px',
                }
              }}
            />
            
            <StyledTextField
              fullWidth
              type={showPassword ? 'text' : 'password'}
              variant="outlined"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Password"
              size={isSmall ? "small" : "medium"}
              margin="normal"
              InputProps={{
                style: { 
                  fontSize: isSmall ? '13px' : '14px',
                },
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      aria-label="toggle password visibility"
                      onClick={handleClickShowPassword}
                      edge="end"
                      size={isSmall ? "small" : "medium"}
                    >
                      {showPassword ? <VisibilityOff fontSize={isSmall ? "small" : "medium"} /> : <Visibility fontSize={isSmall ? "small" : "medium"} />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />
            
            <Box 
              sx={{ 
                display: 'flex', 
                justifyContent: 'space-between', 
                alignItems: 'center', 
                mb: 2,
                flexDirection: { xs: isSmall ? 'column' : 'row', sm: 'row' },
                gap: { xs: isSmall ? 1 : 0, sm: 0 },
                mt: 1
              }}
            >
              <FormControlLabel
                control={
                  <Checkbox
                    checked={rememberMe}
                    onChange={(e) => setRememberMe(e.target.checked)}
                    name="rememberMe"
                    size={isSmall ? "small" : "medium"}
                    sx={{ 
                      color: '#ff9800',
                      '&.Mui-checked': {
                        color: '#ff9800',
                      },
                    }}
                  />
                }
                label={<Typography variant="body2" sx={{ fontSize: { xs: '0.75rem', sm: '0.875rem' } }}>Remember me</Typography>}
              />
              <Link 
                to="/forgot-password" 
                style={{ 
                  color: '#ff9800', 
                  textDecoration: 'none', 
                  fontSize: isSmall ? '12px' : '14px',
                  marginLeft: isSmall ? '0' : 'auto'
                }}
              >
                Forgot password?
              </Link>
            </Box>
            
            <StyledButton
              type="submit"
              fullWidth
              variant="contained"
              disabled={isLoading}
              sx={{ 
                mt: { xs: 0, sm: 1 },
                mb: { xs: 2, sm: 3 },
                fontSize: { xs: '0.875rem', sm: '1rem' },
                py: { xs: 1, sm: 1.25 }
              }}
            >
              Sign In
            </StyledButton>
            
            <Divider sx={{ my: { xs: 1.5, sm: 2 } }}>
              <Typography 
                variant="body2" 
                color="textSecondary" 
                sx={{ 
                  px: 1,
                  fontSize: { xs: '0.75rem', sm: '0.875rem' }
                }}
              >
                Or continue with
              </Typography>
            </Divider>
            
            <Stack 
              direction="row" 
              spacing={2} 
              justifyContent="center" 
              sx={{ 
                my: { xs: 1.5, sm: 2 }
              }}
            >
              <IconButton 
                sx={{ 
                  color: '#DB4437', 
                  border: '1px solid #eee', 
                  borderRadius: '50%',
                  width: { xs: 32, sm: 40 },
                  height: { xs: 32, sm: 40 }
                }}
              >
                <GoogleIcon fontSize={isSmall ? "small" : "medium"} />
              </IconButton>
              <IconButton 
                sx={{ 
                  color: '#333', 
                  border: '1px solid #eee', 
                  borderRadius: '50%',
                  width: { xs: 32, sm: 40 },
                  height: { xs: 32, sm: 40 }
                }}
              >
                <GitHubIcon fontSize={isSmall ? "small" : "medium"} />
              </IconButton>
              <IconButton 
                sx={{ 
                  color: '#0A66C2', 
                  border: '1px solid #eee', 
                  borderRadius: '50%',
                  width: { xs: 32, sm: 40 },
                  height: { xs: 32, sm: 40 }
                }}
              >
                <LinkedInIcon fontSize={isSmall ? "small" : "medium"} />
              </IconButton>
            </Stack>
            
            <Box sx={{ textAlign: 'center', mt: { xs: 2, sm: 3 } }}>
              <Typography 
                variant="body2" 
                color="textSecondary"
                sx={{ fontSize: { xs: '0.75rem', sm: '0.875rem' } }}
              >
                Don't have an account?{' '}
                <Link to="/register" style={{ color: '#ff9800', textDecoration: 'none', fontWeight: 'bold' }}>
                  Sign up now!
                </Link>
              </Typography>
            </Box>
          </Box>
        </StyledPaper>
      </Box>

      {/* Right side with white background and graphics */}
      <Box
        sx={{
          flex: 1,
          background: 'white',
          position: 'relative',
          display: { xs: 'none', md: 'flex' },
          justifyContent: 'center',
          alignItems: 'center',
          overflow: 'hidden'
        }}
      >
        {/* Background gradient overlay */}
        <GradientOverlay />
        
        {/* Animated decorative elements */}
        <FloatingLine width="80px" top="15%" left="10%" color="#FFA726" rotate={0} delay={0.5} />
        <FloatingLine width="120px" top="10%" left="30%" color="#666" rotate={0} delay={1.2} />
        
        <FloatingCircle size="120px" top="25%" left="25%" color="rgba(255, 229, 210, 0.6)" delay={0.3} />
        <FloatingCircle size="140px" top="75%" right="15%" color="rgba(255, 152, 0, 0.3)" delay={1.5} />
        <FloatingCircle size="80px" top="45%" left="65%" color="rgba(255, 87, 34, 0.2)" delay={0.7} />
        
        <FloatingSquare size="40px" top="25%" right="30%" color="#FF9800" delay={1} />
        <FloatingSquare size="20px" top="50%" left="20%" color="#000" delay={2} />
        
        <FloatingLine width="150px" top="85%" left="40%" color="#FFA726" rotate={0} delay={0.8} />
        <FloatingCircle size="40px" top="80%" left="30%" color="#FF5722" delay={1.3} />
        
        {/* Central content */}
        <Box sx={{ 
          maxWidth: '460px', 
          textAlign: 'center',
          zIndex: 1,
          padding: 4,
          position: 'relative'
        }}>
          <Typography variant="h3" sx={{ 
            fontWeight: 700, 
            mb: 2,
            color: '#333',
            position: 'relative'
          }}>
            {/* Monitor AI Healthcare */}
          </Typography>
          <Typography variant="body1" sx={{ 
            color: '#666',
            mb: 2,
            lineHeight: 1.7,
            position: 'relative'
          }}>
            {/* Securely access your AI monitoring dashboard to ensure patient safety and regulatory compliance for healthcare applications. */}
          </Typography>
        </Box>
      </Box>

      {/* Add a simplified version of the right panel for mobile view */}
      <Box
        sx={{
          display: { xs: 'flex', md: 'none' },
          justifyContent: 'center',
          alignItems: 'center',
          background: 'linear-gradient(180deg, rgba(255,255,255,1) 0%, rgba(255,152,0,0.1) 100%)',
          p: 3,
          minHeight: '120px',
          textAlign: 'center'
        }}
      >
        <Typography
          variant="h6"
          sx={{
            fontWeight: 600,
            color: '#333',
            position: 'relative',
            mb: 1
          }}
        >
          Monitor AI Healthcare
        </Typography>
        <Typography
          variant="body2"
          sx={{
            color: '#666',
            fontSize: { xs: '0.75rem', sm: '0.875rem' }
          }}
        >
          Securely access your AI monitoring dashboard 
        </Typography>
      </Box>
    </Box>
  );
};

export default Login;