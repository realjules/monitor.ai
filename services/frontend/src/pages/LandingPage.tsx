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
  IconButton,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
} from '@mui/material';
import { Link } from 'react-router-dom';
import { styled } from '@mui/material/styles';
import { Menu as MenuIcon } from '@mui/icons-material';

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
        fontSize: { xs: '1rem', sm: '1.25rem' },
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
  [theme.breakpoints.down('sm')]: {
    padding: '8px 16px',
    fontSize: '0.875rem',
  },
}));

const TaglineChip = styled(Chip)(({ theme }) => ({
  backgroundColor: 'rgba(255, 152, 0, 0.1)',
  color: theme.palette.primary.main,
  fontWeight: 600,
  borderRadius: '16px',
  height: '32px',
  [theme.breakpoints.down('sm')]: {
    height: '28px',
    fontSize: '0.75rem',
  },
}));

const HeroContainer = styled(Box)(({ theme }) => ({
  backgroundColor: theme.palette.background.paper,
  padding: theme.spacing(8, 0, 10),
  position: 'relative',
  overflow: 'hidden',
  borderRadius: '0 0 40px 40px',
  [theme.breakpoints.down('md')]: {
    padding: theme.spacing(6, 0, 8),
  },
  [theme.breakpoints.down('sm')]: {
    padding: theme.spacing(4, 0, 6),
  },
}));

// LandingPage component
const LandingPage = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const isSmall = useMediaQuery(theme.breakpoints.down('sm'));
  const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false);

  const toggleMobileMenu = () => {
    setMobileMenuOpen(!mobileMenuOpen);
  };

  return (
    <Box sx={{ bgcolor: 'background.default', minHeight: '100vh' }}>
      <StyledAppBar>
        <Container maxWidth="lg">
          <Toolbar disableGutters sx={{ justifyContent: 'space-between' }}>
            <Logo />
            
            {isMobile ? (
              <>
                <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
                  <NavButton 
                    component={Link} 
                    to="/login"
                    sx={{ 
                      display: { xs: 'none', sm: 'flex' },
                      fontSize: { xs: '0.875rem', sm: '1rem' },
                      minWidth: 'auto',
                      px: 1.5
                    }}
                  >
                    Sign In
                  </NavButton>
                  <DemoButton 
                    variant="contained" 
                    component={Link} 
                    to="/request-demo"
                    size={isSmall ? "small" : "medium"}
                    sx={{ 
                      whiteSpace: 'nowrap',
                      px: isSmall ? 1.5 : 2.5,
                      py: isSmall ? 0.5 : 1,
                      fontSize: { xs: '0.75rem', sm: '0.875rem' }
                    }}
                  >
                    Request a demo
                  </DemoButton>
                  <IconButton
                    size="medium"
                    edge="end"
                    color="inherit"
                    aria-label="menu"
                    onClick={toggleMobileMenu}
                    sx={{ ml: 1 }}
                  >
                    <MenuIcon />
                  </IconButton>
                </Box>
                <Drawer 
                  anchor="right" 
                  open={mobileMenuOpen} 
                  onClose={toggleMobileMenu}
                  sx={{
                    '& .MuiDrawer-paper': {
                      width: { xs: '75%', sm: '50%' },
                      maxWidth: '300px',
                    }
                  }}
                >
                  <Box sx={{ p: 2 }}>
                    <Typography variant="h6" component="div" sx={{ mb: 2 }}>
                      Menu
                    </Typography>
                    <List>
                      {['Home', 'About', 'Services', 'Sign In'].map((text) => (
                        <ListItem key={text} disablePadding>
                          <ListItemButton
                            component={Link}
                            to={text === 'Home' ? '/' : `/${text.toLowerCase().replace(' ', '-')}`}
                            onClick={toggleMobileMenu}
                          >
                            <ListItemText primary={text} />
                          </ListItemButton>
                        </ListItem>
                      ))}
                    </List>
                  </Box>
                </Drawer>
              </>
            ) : (
              <>
                <Box sx={{ display: 'flex', gap: 2 }}>
                  <NavButton component={Link} to="/">Home</NavButton>
                  <NavButton component={Link} to="/about">About</NavButton>
                  <NavButton component={Link} to="/services">Services</NavButton>
                  <NavButton component={Link} to="/login">Sign In</NavButton>
                </Box>
                <DemoButton 
                  variant="contained" 
                  component={Link} 
                  to="/request-demo"
                >
                  Request a demo
                </DemoButton>
              </>
            )}
          </Toolbar>
        </Container>
      </StyledAppBar>

      <HeroContainer>
        <Container maxWidth="lg">
          <Box 
            sx={{ 
              display: 'flex', 
              flexDirection: isMobile ? 'column' : 'row', 
              gap: { xs: 3, sm: 4, md: 6 }, 
              alignItems: 'center',
              px: { xs: 2, sm: 3, md: 0 }
            }}
          >
            <Box sx={{ flex: 1, maxWidth: isMobile ? '100%' : '60%' }}>
              <TaglineChip label="Make AI Safe for Healthcare" />
              
              <Typography 
                variant="h1" 
                component="h1"
                sx={{ 
                  fontSize: { xs: '1.75rem', sm: '2.5rem', md: '3.5rem', lg: '4rem' },
                  fontWeight: 700,
                  lineHeight: 1.2,
                  mt: { xs: 2, sm: 3 },
                  mb: { xs: 2, sm: 3 }
                }}
              >
                Make AI Safe for Healthcare
              </Typography>
              
              <Typography 
                variant="body1"
                sx={{ 
                  fontSize: { xs: '0.875rem', sm: '1rem', md: '1.1rem' },
                  color: 'text.secondary',
                  mb: { xs: 3, sm: 4 },
                  maxWidth: '90%'
                }}
              >
                Transform healthcare with AI you can trust. Our monitoring system ensures patient safety, 
                data privacy, and regulatory compliance. Empower healthcare professionals with confidence in AI tools.
              </Typography>
              
              <Box 
                sx={{ 
                  display: 'flex', 
                  gap: { xs: 1, sm: 2 }, 
                  mb: { xs: 3, sm: 4 },
                  flexDirection: { xs: isSmall ? 'column' : 'row', md: 'row' },
                  width: isSmall ? '100%' : 'auto'
                }}
              >
                <DemoButton 
                  variant="contained" 
                  size={isSmall ? "medium" : "large"}
                  component={Link}
                  to="/request-demo"
                  fullWidth={isSmall}
                  sx={{
                    fontSize: { xs: '0.875rem', sm: '1rem' }
                  }}
                >
                  Request a demo
                </DemoButton>
                <Button 
                  variant="outlined" 
                  size={isSmall ? "medium" : "large"}
                  component={Link}
                  to="/learn-more"
                  fullWidth={isSmall}
                  sx={{ 
                    borderRadius: '24px',
                    textTransform: 'none',
                    fontWeight: 600,
                    borderColor: theme.palette.primary.main,
                    fontSize: { xs: '0.875rem', sm: '1rem' }
                  }}
                >
                  Learn more
                </Button>
              </Box>
              
              <Box 
                sx={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: { xs: 2, sm: 3 },
                  flexWrap: { xs: 'wrap', sm: 'nowrap' }
                }}
              >
                <Stack direction="row" spacing={-1}>
                  {[1, 2, 3, 4].map((item) => (
                    <Avatar 
                      key={item}
                      sx={{ 
                        width: { xs: 28, sm: 36 }, 
                        height: { xs: 28, sm: 36 },
                        border: `2px solid ${theme.palette.background.paper}`
                      }}
                    />
                  ))}
                </Stack>
                
                <Box>
                  <Typography 
                    variant="subtitle1" 
                    fontWeight={600}
                    sx={{ fontSize: { xs: '0.875rem', sm: '1rem' } }}
                  >
                    Rated 4.9/5
                  </Typography>
                  <Typography 
                    variant="body2" 
                    color="text.secondary"
                    sx={{ fontSize: { xs: '0.75rem', sm: '0.875rem' } }}
                  >
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
                position: 'relative',
                width: '100%',
                mt: isMobile ? 4 : 0
              }}
            >
              {/* Placeholder for the healthcare AI image */}
              <Box
                sx={{
                  width: { xs: '100%', sm: '90%', md: '400px' },
                  height: { xs: '200px', sm: '250px', md: '400px' },
                  bgcolor: 'rgba(255, 152, 0, 0.1)',
                  borderRadius: '20px',
                  display: 'flex',
                  justifyContent: 'center',
                  alignItems: 'center',
                }}
              >
                <Typography 
                  variant="body1" 
                  color="text.secondary"
                  sx={{ fontSize: { xs: '0.75rem', sm: '0.875rem', md: '1rem' } }}
                >
                  Your AI Healthcare Image Here
                </Typography>
              </Box>
              
              {/* Stats card */}
              <Card
                sx={{
                  position: 'absolute',
                  bottom: { xs: -15, sm: -20 },
                  right: { xs: '10%', sm: '20%', md: 0 },
                  width: { xs: '140px', sm: '160px', md: '180px' },
                  borderRadius: '16px',
                  boxShadow: '0 8px 24px rgba(0, 0, 0, 0.1)',
                }}
              >
                <CardContent sx={{ py: { xs: 1.5, sm: 2 } }}>
                  <Typography 
                    variant="h5" 
                    fontWeight={700} 
                    color={theme.palette.primary.main}
                    sx={{ fontSize: { xs: '1.25rem', sm: '1.5rem' } }}
                  >
                    250+
                  </Typography>
                  <Typography 
                    variant="body2" 
                    color="text.secondary"
                    sx={{ fontSize: { xs: '0.75rem', sm: '0.875rem' } }}
                  >
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