import React from 'react';
import {
  Box,
  Button,
  Container,
  Typography,
  AppBar,
  Toolbar,
  useMediaQuery,
  useTheme,
  Card,
  CardContent,
  Stack,
  Avatar,
  Chip,
} from '@mui/material';
import { Link } from 'react-router-dom';
import { styled } from '@mui/material/styles';

// Logo component
const Logo = () => (
  <Box sx={{ display: 'flex', alignItems: 'center' }}>
    <svg width="40" height="40" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="10" y="10" width="20" height="20" stroke="#FF9800" strokeWidth="4" fill="none" />
      <rect x="50" y="20" width="20" height="20" stroke="#FF9800" strokeWidth="4" fill="none" />
      <rect x="70" y="40" width="20" height="20" stroke="#FF9800" strokeWidth="4" fill="none" />
      <rect x="20" y="50" width="30" height="30" stroke="#FF9800" strokeWidth="4" fill="none" />
      <rect x="40" y="60" width="20" height="20" stroke="#FF9800" strokeWidth="4" fill="none" />
    </svg>
    <Typography
      variant="h6"
      component="div"
      sx={{
        ml: 1,
        fontWeight: 700,
        color: 'text.primary',
        textDecoration: 'none',
      }}
    >
      monitor ai
    </Typography>
  </Box>
);

// Custom styled components
const StyledAppBar = styled(AppBar)(({ theme }) => ({
  backgroundColor: 'transparent',
  boxShadow: 'none',
  borderBottom: `1px solid ${theme.palette.divider}`,
  position: 'static',
}));

const NavButton = styled(Button)(({ theme }) => ({
  textTransform: 'none',
  color: theme.palette.text.primary,
  fontSize: '1rem',
  '&:hover': {
    backgroundColor: 'transparent',
    color: theme.palette.primary.main,
  },
}));

const DemoButton = styled(Button)(({ theme }) => ({
  backgroundColor: theme.palette.primary.main,
  color: theme.palette.common.white,
  borderRadius: '24px',
  padding: '10px 24px',
  textTransform: 'none',
  fontWeight: 600,
  '&:hover': {
    backgroundColor: theme.palette.primary.dark,
  },
}));

const TaglineChip = styled(Chip)(({ theme }) => ({
  backgroundColor: 'rgba(255, 152, 0, 0.1)',
  color: theme.palette.primary.main,
  fontWeight: 600,
  borderRadius: '16px',
  height: '32px',
}));

const HeroContainer = styled(Box)(({ theme }) => ({
  backgroundColor: theme.palette.background.paper,
  padding: theme.spacing(8, 0, 10),
  position: 'relative',
  overflow: 'hidden',
  borderRadius: '0 0 40px 40px',
}));

// LandingPage component
const LandingPage = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  return (
    <Box sx={{ bgcolor: 'background.default', minHeight: '100vh' }}>
      <StyledAppBar>
        <Container maxWidth="lg">
          <Toolbar disableGutters sx={{ justifyContent: 'space-between' }}>
            <Logo />
            
            {!isMobile && (
              <Box sx={{ display: 'flex', gap: 2 }}>
                <NavButton component={Link} to="/">Home</NavButton>
                <NavButton component={Link} to="/about">About</NavButton>
                <NavButton component={Link} to="/services">Services</NavButton>
                <NavButton component={Link} to="/login">Sign In</NavButton>
              </Box>
            )}
            
            <DemoButton variant="contained" component={Link} to="/request-demo">Request a demo</DemoButton>
          </Toolbar>
        </Container>
      </StyledAppBar>

      <HeroContainer>
        <Container maxWidth="lg">
          <Box sx={{ display: 'flex', flexDirection: isMobile ? 'column' : 'row', gap: 6, alignItems: 'center' }}>
            <Box sx={{ flex: 1, maxWidth: isMobile ? '100%' : '60%' }}>
              <TaglineChip label="Make AI Safe for Healthcare" />
              
              <Typography 
                variant="h1" 
                component="h1"
                sx={{ 
                  fontSize: isMobile ? '2.5rem' : '4rem',
                  fontWeight: 700,
                  lineHeight: 1.2,
                  mt: 3,
                  mb: 3
                }}
              >
                Make AI Safe for Healthcare
              </Typography>
              
              <Typography 
                variant="body1"
                sx={{ 
                  fontSize: '1.1rem',
                  color: 'text.secondary',
                  mb: 4,
                  maxWidth: '90%'
                }}
              >
                Transform healthcare with AI you can trust. Our monitoring system ensures patient safety, 
                data privacy, and regulatory compliance. Empower healthcare professionals with confidence in AI tools.
              </Typography>
              
              <Box sx={{ display: 'flex', gap: 2, mb: 4 }}>
                <DemoButton 
                  variant="contained" 
                  size="large"
                  component={Link}
                  to="/request-demo"
                >
                  Request a demo
                </DemoButton>
                <Button 
                  variant="outlined" 
                  size="large"
                  component={Link}
                  to="/learn-more"
                  sx={{ 
                    borderRadius: '24px',
                    textTransform: 'none',
                    fontWeight: 600,
                    borderColor: theme.palette.primary.main
                  }}
                >
                  Learn more
                </Button>
              </Box>
              
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 3 }}>
                <Stack direction="row" spacing={-1}>
                  {[1, 2, 3, 4].map((item) => (
                    <Avatar 
                      key={item}
                      sx={{ 
                        width: 36, 
                        height: 36,
                        border: `2px solid ${theme.palette.background.paper}`
                      }}
                    />
                  ))}
                </Stack>
                
                <Box>
                  <Typography variant="subtitle1" fontWeight={600}>
                    Rated 4.9/5
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    by 500+ Healthcare Providers
                  </Typography>
                </Box>
              </Box>
            </Box>
            
            {/* This is where you'll place your image */}
            <Box 
              sx={{ 
                flex: 1,
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                position: 'relative'
              }}
            >
              {/* Placeholder for the healthcare AI image */}
              <Box
                sx={{
                  width: isMobile ? '100%' : '400px',
                  height: isMobile ? '300px' : '400px',
                  bgcolor: 'rgba(255, 152, 0, 0.1)',
                  borderRadius: '20px',
                  display: 'flex',
                  justifyContent: 'center',
                  alignItems: 'center',
                }}
              >
                <Typography variant="body1" color="text.secondary">
                  Your AI Healthcare Image Here
                </Typography>
              </Box>
              
              {/* Stats card */}
              <Card
                sx={{
                  position: 'absolute',
                  bottom: -20,
                  right: isMobile ? '20%' : 0,
                  width: '180px',
                  borderRadius: '16px',
                  boxShadow: '0 8px 24px rgba(0, 0, 0, 0.1)',
                }}
              >
                <CardContent>
                  <Typography variant="h5" fontWeight={700} color={theme.palette.primary.main}>
                    250+
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Healthcare systems protected
                  </Typography>
                </CardContent>
              </Card>
            </Box>
          </Box>
        </Container>
      </HeroContainer>
    </Box>
  );
};

export default LandingPage;