pipeline {
    agent any
/*    environment {
        GITHUB_AUTH_TOKEN = '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'
        }*/
    stages {
        stage('Get-depcheck') {
            steps {
                sh 'wget https://github.com/jeremylong/DependencyCheck/releases/download/v7.1.1/dependency-check-7.1.1-release.zip'
                sh 'unzip -n dependency-check-7.1.1-release.zip'
            }
        }
        stage ('prep-env') {
            steps {
                sh 'mkdir -p reports/nixpkgs'
                sh 'mkdir -p reports/spectrum'
                sh 'mkdir -p reports/nixpkgs-spectrum'
            }
        }
        stage('Dep-Check') {
            parallel {
                stage('Dep-Check-nixpkgs') {
                    steps {
                        sh 'dependency-check/bin/dependency-check.sh --project "NixPkgs" --scan "nixpkgs/" --out ./reports/nixpkgs'
                    }
                }
                stage('Dep-Check-Spectrum') {
                    steps {
                        sh 'dependency-check/bin/dependency-check.sh --project "Spectrum" --scan "spectrum/" --out ./reports/spectrum'
                    }
                }
                stage('Dep-Check-nixpkgs-spectrum') {
                    steps {
                        sh 'dependency-check/bin/dependency-check.sh --project "NixPkgs-Spectrum" --scan "nixpkgs-spectrum" --out ./reports/nixpkgs-spectrum'
                    }
                }
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: './reports/*'
        }
    }
}

