provider "aws" {
  region = var.region
}

data "aws_eks_cluster" "cluster" {
  name = module.eks.cluster_id
}

data "aws_eks_cluster_auth" "cluster" {
  name = module.eks.cluster_id
}

provider "kubernetes" {
  host                   = data.aws_eks_cluster.cluster.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority.0.data)
  token                  = data.aws_eks_cluster_auth.cluster.token
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 18.0"

  cluster_name    = var.cluster_name
  cluster_version = var.cluster_version

  vpc_id     = var.vpc_id
  subnet_ids = var.subnet_ids

  enable_irsa = true

  eks_managed_node_groups = {
    general = {
      desired_size = var.node_groups.general.desired_size
      max_size     = var.node_groups.general.max_size
      min_size     = var.node_groups.general.min_size

      instance_types = var.node_groups.general.instance_types
      capacity_type  = "ON_DEMAND"

      labels = {
        Environment = var.environment
        NodeGroup   = "general"
      }

      tags = {
        Environment = var.environment
        NodeGroup   = "general"
      }
    }

    gpu = {
      desired_size = var.node_groups.gpu.desired_size
      max_size     = var.node_groups.gpu.max_size
      min_size     = var.node_groups.gpu.min_size

      instance_types = var.node_groups.gpu.instance_types
      capacity_type  = "ON_DEMAND"

      labels = {
        Environment = var.environment
        NodeGroup   = "gpu"
      }

      taints = [{
        key    = "nvidia.com/gpu"
        value  = "true"
        effect = "NO_SCHEDULE"
      }]

      tags = {
        Environment = var.environment
        NodeGroup   = "gpu"
      }
    }
  }

  tags = {
    Environment = var.environment
    Terraform   = "true"
  }
}